import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from .models import Post,Profile,Tag

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class ProfileType(DjangoObjectType):
    class Meta:
        model= Profile

class TagType(DjangoObjectType):
    class Meta:
        model=Tag

class PostType(DjangoObjectType):
    class Meta:
        model=Post

class Query(graphene.ObjectType):
    all_posts=graphene.List(PostType)
    author_by_username=graphene.Field(ProfileType,user=graphene.String())
    post_by_slug=graphene.Field(PostType,slug=graphene.String())
    post_by_author=graphene.Field(PostType,user=graphene.String())
    posts_by_tag = graphene.List(PostType, tag=graphene.String())

    def resolve_all_posts(root, info):
        return (
            Post.objects.prefetch_related("tags")
            .select_related("author")
            .all()
        )

    def resolve_author_by_username(root, info, user):
        return Profile.objects.select_related("user").get(
            user__user=user
        )

    def resolve_post_by_slug(root, info, slug):
        return (
            Post.objects.prefetch_related("tags")
            .select_related("author")
            .get(slug=slug)
        )

    def resolve_posts_by_author(root, info, user):
        return (
            Post.objects.prefetch_related("tags")
            .select_related("author")
            .filter(author__user__user=user)
        )

    def resolve_posts_by_tag(root, info, tag):
        return (
            Post.objects.prefetch_related("tags")
            .select_related("author")
            .filter(tags__name__iexact=tag)
        )
        

schema = graphene.Schema(query=Query)



    

