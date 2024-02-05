from django.urls import path
from app.views import register,waste_collection_point,waste_collection_record,wallet,signin,saved_address,update_profile,records,smsPin
from app.views import get_user
from .utils.TokenObtainPairView import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    TokenRefreshView,
)

from app.views import test

urlpatterns = [
    path('getUser/',get_user.GetPersonalDetails),
    path('getalluser/',get_user.GetUserALL),
    path('getWasteUser/',get_user.GetUserWasteCollector),
    path('getDistrictUser/',get_user.GetUserDistrictCollector),
    # path('getStateUser/',get_user.GetUserStateCollector),
    path('registerUser/',register.RegisterAPI.as_view()),
    path('update_profile/',update_profile.UpdateProfileAPI.as_view()),
    path('waste_collection_point/', waste_collection_point.WasteCollectionPointAPI.as_view()),
    path('waste_collection_point/<slug:collection_point_id>/', waste_collection_point.WasteCollectionPointSlugAPI.as_view(), name='login'),
    path('waste_collection_record/',waste_collection_record.WasteCollectionRecordAPI.as_view()),
    path('wallet/',wallet.CreditAPI.as_view()),
    path('wallet/',wallet.DebitAPI.as_view()),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', signin.LoginAPI.as_view(), name='login'),
    path('address/', saved_address.SavedAddressAPI.as_view(), name='login'),
    path('address/<slug:saved_address_id>/', saved_address.SavedAddressSlugAPI.as_view(), name='login'),
    path('test/', test.testFun),
    path('records/<slug:collection_point_id>/', records.WasteCollectionRecordAPI.as_view()),
    path('records/', records.RecordsAPI.as_view()),
    path('record/<slug:record_id>/', records.RecordsInfoAPI.as_view()),
    path('record/<slug:record_id>/items/', records.ItemInfoAPI.as_view()),
    path('pin_verify/<slug:collection_point_id>/', smsPin.SmsPinAPI.as_view()),
]

