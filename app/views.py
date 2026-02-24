
from datetime import datetime
from django.db import transaction
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Train, Booking, SearchLog
from .serializers import UserSerializer, TrainSerializer, BookingSerializer


class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'ADMIN')
    
class IsUserRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'USER')    

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        "message": "User Registered Successfully",
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "role": user.role 
                    }, status=201)
            except Exception as e:
                return Response({"error": e}, status=500)
                
        return Response(serializer.errors, status=500)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "role": user.role,
                "name": user.first_name
            }, status=200)
        return Response({"error": "Invalid email or password"}, status=401)



class TrainView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminRole()]
        return [permissions.IsAuthenticated()]

    def post(self, request):
        serializer = TrainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    



class TrainSearchView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        start_time = datetime.now()

        
        source = request.query_params.get('source')
        destination = request.query_params.get('destination')
        date_str = request.query_params.get('date') 
        limit = int(request.query_params.get('limit', 10))
        offset = int(request.query_params.get('offset', 0))

       
        filters = {}
        if source: filters['source__iexact'] = source
        if destination: filters['destination__iexact'] = destination
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                filters['departure_time__date'] = date_obj
            except ValueError:
                pass 

        trains = Train.objects.filter(**filters)[offset:offset+limit]
        serializer = TrainSerializer(trains, many=True)
        duration = datetime.now() - start_time

        execution_time = duration.total_seconds()

        if source and destination and len(source.strip()) > 0:
            SearchLog.objects.using('mongodb').create(
            endpoint=request.path,
            source=source,
            destination=destination,
            params=request.query_params.dict(),
            user_id=getattr(request.user, 'id', None),
            execution_time=execution_time,
            timestamp=datetime.now()
        )
       

        return Response(serializer.data)



class BookingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        train_id = request.data.get('train_id')
        seats_required = int(request.data.get('seats', 1))

        try:
            with transaction.atomic():
                train = Train.objects.select_for_update().get(id=train_id)
                
                if train.available_seats >= seats_required:
                    train.available_seats -= seats_required
                    train.save()
                    
                    booking = Booking.objects.create(
                        user=request.user,
                        train=train,
                        seats_booked=seats_required
                    )
                    return Response({"message": "Booking successful", "booking_id": booking.id}, status=201)
                else:
                    return Response({"error": "Not enough seats available"}, status=400)
        except Train.DoesNotExist:
            return Response({"error": "Train not found"}, status=400)

class MyBookingsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)


class AnalyticsTopRoutesView(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request):
        top_routes = (SearchLog.objects.using('mongodb')
                      .exclude(source="")
                      .exclude(destination="")
                      .exclude(source__isnull=True)
                      .exclude(destination__isnull=True)
                      .values('source', 'destination')
                      .annotate(search_count=Count('id'))
                      .order_by('-search_count')[:5])
        return Response(list(top_routes))
    
class SystemLogsView(APIView):
 
    permission_classes = [IsAdminRole]

    def get(self, request):
      
        logs = SearchLog.objects.using('mongodb').all().order_by('-id')[:20]
        
        data = [{
            "user_id": log.user_id,
            "source": log.source,
            "destination": log.destination,
            "execution_time": f"{log.execution_time:.4f}s",
            "timestamp": log.id.generation_time.strftime("%Y-%m-%d %H:%M:%S") if hasattr(log.id, 'generation_time') else "N/A"
        } for log in logs]
        
        return Response(data)  