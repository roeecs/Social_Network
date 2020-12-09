from .models import Post
from rest_framework import serializers
from rest_framework.exceptions import APIException
from django.contrib.auth.models import User
from pyhunter import PyHunter
import clearbit


CLBT_KEY = "sk_b3f5f9bb4fe2d6f6b3eedfad56fba4d0"
HUNTER_KEY = '099b9c5c086188eee014fabf5805ad413e839479'
hunter = PyHunter(HUNTER_KEY)
clearbit.key = CLBT_KEY


class UserSerializer(serializers.ModelSerializer):
    """
        User Serializer, allows us to add and verify data
    """
    def create(self, validated_data):
        first_name = ""
        last_name = ""
        email = None

        if 'email' in validated_data:
            email = validated_data['email']

            val_resp = hunter.email_verifier(email)
            if val_resp['status'] == 'invalid':
                raise APIException("Invalid email!")

            enr_resp = clearbit.Enrichment.find(email=email, stream=True)
            if 'person' in enr_resp:
                if 'name' in enr_resp['person']:
                    if 'givenName' in enr_resp['person']['name']:
                        first_name = enr_resp['person']['name']['givenName']
                    if 'familyName' in enr_resp['person']['name']:
                        last_name = enr_resp['person']['name']['familyName']

        user = User.objects.create_user(username=validated_data['username'],
                                        email=email,
                                        first_name=first_name,
                                        last_name=last_name)
        #   perhaps add a try cath for password
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', )
        write_only_fields = ('password',)
        read_only_fields = ('id',)



