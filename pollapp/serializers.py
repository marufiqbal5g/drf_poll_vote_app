from rest_framework import serializers
from .models import Question, Choice
from django.contrib.auth.models import User


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'votes']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(source='choice_set', many=True, read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'user', 'choices']


# CREATE SERIALIZERS
class ChoiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['choice_text']


class QuestionCreateSerializer(serializers.ModelSerializer):
    choices = ChoiceCreateSerializer(many=True)

    class Meta:
        model = Question
        fields = ['question_text', 'choices']

    def create(self, validated_data):
        choices_data = validated_data.pop('choices')

        question = Question.objects.create(
            user=self.context['request'].user,
            **validated_data
        )

        for choice_data in choices_data:
            Choice.objects.create(
                question=question,
                **choice_data
            )

        return question
    
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )

        return user