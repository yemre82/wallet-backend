from rest_framework_simplejwt.tokens import RefreshToken
from users.models import JWTToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    # İlgili kullanıcıya ait mevcut bir JWTToken nesnesini kontrol edin
    existing_token = JWTToken.objects.filter(user=user).first()

    # Eğer mevcut bir JWTToken nesnesi varsa, bu nesneyi güncelle
    if existing_token:
        existing_token.access_token = str(refresh.access_token)
        existing_token.refresh_token = str(refresh)
        existing_token.save()
    else:
        # Eğer mevcut bir nesne yoksa, yeni bir nesne oluştur
        JWTToken.objects.create(
            user=user,
            access_token=str(refresh.access_token),
            refresh_token=str(refresh)
        )

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
