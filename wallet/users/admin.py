from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser, JWTToken
from rest_framework_simplejwt.tokens import RefreshToken

# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('id','email', 'phone', 'firstname', 'lastname', 'is_staff', 'is_admin', 'is_active')
    search_fields = ('email', 'phone', 'firstname', 'lastname')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('email',)
admin.site.register(CustomUser, CustomUserAdmin)

class JWTTokenAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'access_token', 'refresh_token', 'created_at']
    search_fields = ('user__email', 'user__phone', 'user__firstname', 'user__lastname')
    readonly_fields = ['access_token', 'refresh_token', 'created_at']
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
    def save_model(self, request, obj, form, change):
        # İlgili kullanıcıya ait mevcut bir JWTToken nesnesini kontrol edin
        existing_token = JWTToken.objects.filter(user=obj.user).first()

        # Yeni tokenler üret
        refresh = RefreshToken.for_user(obj.user)
        
        # Eğer mevcut bir JWTToken nesnesi varsa, bu nesneyi güncelle
        if existing_token:
            existing_token.access_token = str(refresh.access_token)
            existing_token.refresh_token = str(refresh)
            existing_token.save()
        else:
            obj.access_token = str(refresh.access_token)
            obj.refresh_token = str(refresh)
            super().save_model(request, obj, form, change)
    
admin.site.register(JWTToken, JWTTokenAdmin)