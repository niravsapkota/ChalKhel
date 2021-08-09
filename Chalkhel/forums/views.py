from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from .models import Profile, Post, Comment, Vote, Forum, ForumMember, Notification
from django.contrib.auth.models import User
from .forms import ProfileForm, PostForm, CommentForm, VoteForm, ForumForm, ForumMemberForm, UserRegisterForm
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, Http404
from django.shortcuts import render, redirect, get_object_or_404

from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, ProfileSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage

# class MyView(LoginRequiredMixin, View):
#     login_url = '/login/'
#     redirect_field_name = 'redirect_to'



def landing(request):
    return render(request, "forums/landing.html")

def get_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(affected_agent=request.user.id)
        notifications.read = notifications.filter(is_read=1)
        notifications.unread = notifications.filter(is_read=0)
        return notifications

def read_all_notifications(request, **kwargs):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(affected_agent=request.user.id)
        for notification in notifications:
            notification.is_read = 1
            notification.save()
        return redirect('login')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'forums/auth/register.html', {'form': form})

def add_voted_or_not(objects, user):
    if user.is_authenticated:
        for object in objects:
            object_number = 0
            liked_object = [value for value in object.votes.all() if value in user.votes.all()]
            if len(liked_object) != 0:
                object.voted = True
                object.vote_type = liked_object[object_number].vote_type
                object_number = object_number + 1
    return objects


class MyProfile(LoginRequiredMixin, DetailView):
    # login_url = '/login'
    # redirect_field_name = '/login'

    @login_required
    def posts(request):
        profile = request.user.profiles
        posts = Post.objects.filter(owner=request.user)
        detailed_posts = add_voted_or_not(posts, request.user)
        return render(request, 'forums/profile/comps/posts.html',
                      {'profile': profile, 'posts': detailed_posts, 'notifications':get_notifications(request)})

    @login_required
    def comments(request):
        profile = request.user.profiles
        comments = Comment.objects.filter(owner=request.user)
        return render(request, 'forums/profile/comps/comments.html',
                      {'profile': profile, 'comments': comments})
    @login_required
    def voted_posts(request):
        profile = request.user.profiles
        voted_posts = []
        votes = request.user.votes.all()
        for vote in votes:
            voted_posts.append(vote.post)
        return render(request, 'forums/profile/comps/posts.html',
                      {'profile': profile, 'posts': voted_posts})
    @login_required
    def hidden_posts(request):
        profile = request.user.profiles
        hidden_posts = Post.objects.filter(owner=request.user, hidden=True)
        return render(request, 'forums/profile/comps/posts.html',
                      {'profile': profile, 'posts': hidden_posts})

    @login_required
    def settings(request):
        profile = request.user.profiles
        hidden_posts = Post.objects.filter(owner=request.user, hidden=True)
        return render(request, 'forums/profile/comps/posts.html',
                      {'profile': profile, 'posts': hidden_posts})


class ProfileListView(ListView):
    model = Profile
    template_name = 'forums/profile/profile_list.html'


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'forums/profile/comps/posts.html'

    def posts(request, slug):
        profile = Profile.objects.get(slug=slug)
        posts = Post.objects.filter(owner=profile.user)
        detailed_posts = add_voted_or_not(posts, request.user)
        return render(request, 'forums/profile/comps/posts.html',
                      {'profile': profile, 'posts': detailed_posts})

    def comments(request, slug):
        profile = Profile.objects.get(slug=slug)
        comments = Comment.objects.filter(owner=profile.user)
        return render(request, 'forums/profile/comps/comments.html',
                      {'profile': profile, 'comments': comments})


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'forums/profile/profile_form.html'


class PostListView(ListView):
    model = Post
    template_name = 'forums/post/post_list.html'


class PostCreateView(CreateView):
    model = Post
    template_name = 'forums/post/post_form.html'
    fields = ['name', 'hidden', 'media_content_type', 'media_content', 'body', 'forum']

    # def get(self, request, slug):
    #     forummembers = ForumMember.objects.filter(member = request.user.id)
    #     forums = []
    #     for member in forummembers:
    #         forums.append(member.forum)
    #     print(forums)
    #     return render(request, self.template_name, {'fields':self.fields})

    def form_valid(self, form):
        file = self.request.FILES['media_content'].name
        form.instance.owner = self.request.user
        if file.endswith('.png') or file.endswith('.jpeg') or file.endswith('.gif') or file.endswith('.jpg'):
            form.instance.media_content_type = 0
        elif file.endswith('.mov') or file.endswith('.qt') or file.endswith('.mp4'):
            form.instance.media_content_type = 1
        else:
            return super().form_invalid(form)

        return super().form_valid(form)

class PostDetailView(DetailView):
    model = Post
    template_name = 'forums/post/post_detail.html'

    def get(self, request, slug):
        post = self.model.objects.get(slug=slug)
        # content_type = ContentType.objects.get_for_model(Post)
        post_vote = post.votes.filter(owner = request.user.id)
        if len(post_vote) != 0:
            post.voted = True
            post.vote_type = post_vote[0].vote_type
            post.vote_id = post_vote[0].id

        comments = post.comments.all()
        content_type_comment = ContentType.objects.get_for_model(Comment)
        comment_vote = Vote.objects.filter(owner=request.user.id, content_type__pk=content_type_comment.id)

        if len(comment_vote) != 0:
            for comment in comments:
                object_number = 0
                if comment_vote[object_number] in comment.votes.all():
                    comment.voted = True
                    comment.vote_type = comment_vote[object_number].vote_type
                    comment.vote_id = comment_vote[object_number].id
                    object_number = object_number + 1

        return render(request, self.template_name, {'object': post, 'comments':comments})


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'forums/post/post_form.html'


class CommentListView(ListView):
    model = Comment
    template_name = 'forums/comment/comment_list.html'


class CommentCreateView(CreateView):
    model = Comment
    # form_class = CommentForm
    template_name = 'forums/comment/comment_form.html'
    fields = ['body','post']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        super().form_valid(form)
        return redirect('forums_post_detail', slug=form.instance.post.slug)


class CommentDetailView(DetailView):
    model = Comment
    template_name = 'forums/comment/comment_detail.html'


class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'forums/comment/comment_form.html'


class VoteListView(ListView):
    model = Vote
    # template_name = 'forums/comment/comment_form.html'


class PostVoteCreateView(CreateView):
    model = Vote
    # form_class = VoteForm
    fields = ['vote_type', 'object_id']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.content_object = Post.objects.get(id=form.instance.object_id)
        super().form_valid(form)
        return redirect('forums_post_detail', slug=form.instance.content_object.slug)

class CommentVoteCreateView(CreateView):
    model = Vote
    # form_class = VoteForm
    fields = ['vote_type', 'object_id']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.content_object = Comment.objects.get(id=form.instance.object_id)
        super().form_valid(form)
        return redirect('forums_post_detail', slug=form.instance.content_object.post.slug)


class VoteDetailView(DetailView):
    model = Vote
    template_name = 'forums/vote/vote_detail.html'

class VoteUpdateView(UpdateView):
    model = Vote
    fields = ['vote_type']

    def get_success_url(self):
    # Assuming there is a ForeignKey from Comment to Post in your model
        if self.object.content_type.model == 'post':
            post = self.object.content_object
            return reverse_lazy( 'forums_post_detail', kwargs={'slug': post.slug})
        else:
            comment = self.object.content_object
            return reverse_lazy( 'forums_post_detail', kwargs={'slug': comment.post.slug})

class VoteDeleteView(DeleteView):
    model = Vote

    def get_success_url(self):
    # Assuming there is a ForeignKey from Comment to Post in your model
        if self.object.content_type.model == 'post':
            post = self.object.content_object
            return reverse_lazy( 'forums_post_detail', kwargs={'slug': post.slug})
        else:
            comment = self.object.content_object
            return reverse_lazy( 'forums_post_detail', kwargs={'slug': comment.post.slug})


class ForumListView(ListView):
    model = Forum
    template_name = 'forums/forum/forum_list.html'


class ForumCreateView(CreateView):
    model = Forum
    # form_class = ForumForm
    template_name = 'forums/forum/forum_form.html'
    fields = ['name', 'bio', 'profile_pic', 'cover_pic']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
        # return redirect('forums_forum_detail', slug=form.instance.slug)


class ForumDetailView(DetailView):
    model = Forum
    template_name = 'forums/forum/comps/posts.html'

    def get(self, request, slug):
        forum = Forum.objects.get(slug=slug)
        posts = Post.objects.filter(forum=forum)
        print(request.user.is_authenticated)
        if request.user.is_authenticated and len(forum.forummembers.filter(member = request.user.id)) != 0:
            forum.member = forum.forummembers.get(member = request.user.id).id
            print(forum.member)
        # comments = Comment.objects.filter(owner=request.user)
        common_users = [value for value in forum.forummembers.all() if value in request.user.forummembers.all()]
        if len(common_users) != 0:
            forum.followed = True
        return render(request, self.template_name, {'forum': forum, 'posts': posts})


class ForumUpdateView(UpdateView):
    model = Forum
    form_class = ForumForm
    template_name = 'forums/forum/forum_form.html'


class ForumMemberListView(ListView):
    model = ForumMember
    template_name = 'forums/forummember/forummember_list.html'


class ForumMemberCreateView(CreateView):
    model = ForumMember
    # form_class = ForumMemberForm
    fields = ['forum']

    def form_valid(self, form):
        form.instance.member = self.request.user
        super().form_valid(form)
        return redirect('forums_forum_detail', slug=form.instance.forum.slug)


class ForumMemberDetailView(DetailView):
    model = ForumMember


class ForumMemberUpdateView(UpdateView):
    model = ForumMember
    form_class = ForumMemberForm

class ForumMemberDeleteView(DeleteView):
    model = ForumMember

    def get_success_url(self):
    # Assuming there is a ForeignKey from Comment to Post in your model
        forum = self.object.forum
        return reverse_lazy( 'forums_forum_detail', kwargs={'slug': forum.slug})





# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
        return super(LoginAPI, self).post(request, format=None)
        return super(LoginAPI, self).post(request, format=None)
