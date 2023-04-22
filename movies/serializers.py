from rest_framework import serializers
from django.core.validators import MaxLengthValidator, MinLengthValidator
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from rest_framework.serializers import ValidationError
from .models import Movie, Review


# def overview_validator(value):
#     if len(value) > 300:
#         raise ValidationError('소개 문구는 최대 300자 이하로 작성해야 합니다.')
#     elif len(value) < 10:
#         raise ValidationError('소개 문구는 최소 10자 이상으로 작성해야 합니다.')
#     return value

# UniqueTogetherValidator()는 두 개 이상의 필드에서 값이 유일한지 확인!
    #  두 개 이상의 필드를 검사하기 때문에 특정 필드의 validators 옵션에 사용할 수 없고 Meta 속성에 추가
    # 이름이 같아도 감상평이 다르면 통과!,
    # validators = [
    #     UniqueTogetherValidator(
    #         queryset=Movie.objects.all(),
    #         fields=['name', 'overview'],
    #     )
    # ]

# 하나의 필드에 대해서만 유효성 검사를 진행하고 싶다면 validate_[필드명]()
    # def validate_overview(self, value):
    #     if 10 <= len(value) and len(value) <= 300:
    #         return value
    #     raise ValidationError('영화 소개는 10자 이상, 300자 이하로 작성해주세요.')


class MovieSerializer(serializers.ModelSerializer):
    # reviews = serializers.PrimaryKeyRelatedField(source='reviews', many=True, read_only=True)
    # Review -> __str__ retrun 값
    # reviews = serializers.StringRelatedField(many=True)
    # review모델 전부 보여주기,ReviewSerializer이 먼저 정의 되어야함
    # reviews = ReviewSerializer(many=True, read_only=True)
    # overview = serializers.CharField(validators=[overview_validator])
    # UniqueValidator()는 특정한 하나의 필드에서 값이 유일한지 확인!
    # 이름이 같으면 무조건 배재!
    name = serializers.CharField(validators=[UniqueValidator(
        queryset=Movie.objects.all(),  # 필수 옵션!
        message='이미 존재하는 영화 이름입니다.',  # 필수 아님!
    )])

    def validate(self, attrs):
        print(attrs)
        if len(attrs['overview']) < 10 or len(attrs['overview']) > 500:
            raise ValidationError('영화 소개는 10자 이상, 500자 이하로 작성해주세요.')
        if len(attrs['name']) > 50:
            raise ValidationError('영화 이름은 50자 이하로 작성해주세요.')
        return attrs

    # ModelSerializer를 사용하면 데이터베이스에서 생성해 주는 필드에 자동으로 read_only 옵션을 넣음
    class Meta:
        model = Movie
        fields = '__all__'
        # 만약 그 외 필드(자동 생성되지 않는 필드)에 선택적으로 read_only를 추가하려면 read_only_fields 옵션을 사용하면 됨
        # read_only_fields = ['name']
        # 다양한 필드에 여러 옵션을 추가해야 할 경우 extra_kwargs를 사용
        # extra_kwargs = {
        #     'overview': {'write_only': True},
        # }
        #  1개 이상 필드의 유효성 검사를 한꺼번에 하려면 validate_[필드명]() 대신 validate()를 사용


    def create(self, validated_data):
        return Movie.objects.create(**validated_data)  # 언패킹

    def update(self, instance, validated_data):
        # patch를 사용 하기 위에 값이 들어 오지 않으면 원래 상태, 아니면 수정된 데이터 저장
        instance.name = validated_data.get('name', instance.name)
        instance.opening_date = validated_data.get('opening_date', instance.opening_date)
        instance.running_time = validated_data.get('running_time', instance.running_time)
        instance.overview = validated_data.get('overview', instance.overview)
        instance.save()
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    # movie = serializers.StringRelatedField()
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'movie', 'username', 'star', 'comment', 'created']
        # extra_kwargs = {
        #     'movie': {'read_only': True},  # 역직렬화 방지!, 영화 정보(id)를 입력받지 않고 URL로 받아올 것이기 때문
        # }