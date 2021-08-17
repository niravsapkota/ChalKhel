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
import datetime
from django.db.models import Count
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
from collections import Counter, OrderedDict
from django.db.models import Case, When
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

def trending_forums():
    week_ago = datetime.date.today() - datetime.timedelta(days = 7)
    forum = ForumMember.objects.filter(created__gte = week_ago).values_list('forum', flat=True)
    result = [item for items, c in Counter(list(forum)).most_common()
                                       for item in [items] * c]
    removed_duplicates = list(dict.fromkeys(result))
    # print( result )
    # print( removed_duplicates )

    order = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(removed_duplicates)])
    # print(order)
    forums =  Forum.objects.filter(pk__in = removed_duplicates).order_by(order).annotate(list_order = order).annotate(num_posts=Count('post')) \
                .order_by('-num_posts', '-list_order')
    return forums[: 4]

def trending_posts():
    week_ago = datetime.date.today() - datetime.timedelta(days = 7)
    posts = Post.objects.filter(created__gte = week_ago).annotate(num_comments=Count('comments')).annotate(num_votes=Count('votes')) \
                .order_by('-num_comments', '-num_votes')
    return posts[: 4]


def search_forum(request):
    forums = Forum.objects.filter(name__icontains=request.GET.get('q'))

    if request.user.is_authenticated:
        followed = forums.filter(pk__in= request.user.forummembers.values_list('forum', flat=True)).values_list('id', flat=True)
        forummembers = request.user.forummembers.values_list('id', flat=True)

        for forum in forums:
            object_number = 0
            followed_forum = [value for value in forum.forummembers.all() if value in request.user.forummembers.all()]
            if len(followed_forum) != 0:
                # forum.followed = True
                forum.forumfollow = followed_forum[object_number].id
                object_number = object_number + 1
        return render(request, 'forums/forum/forum_list.html', {'object_list':forums, 'followed_id':followed, 'forummembers':forummembers})

    return render(request, 'forums/forum/forum_list.html', {'object_list':forums})


def feed(request):
    if request.user.is_authenticated:
        followed = Forum.objects.filter(pk__in= request.user.forummembers.values_list('forum', flat=True)).values_list('id', flat=True)
        posts = Post.objects.filter(forum__in=followed).order_by('-created')
        detailed_posts = add_voted_or_not(posts, request.user)

        followed = ForumMember.objects.filter(member = request.user).values_list('forum', flat = True);
        followed = Forum.objects.filter(pk__in = followed)

        return render(request, 'forums/profile/comps/feed.html',
                      {'posts': detailed_posts, 'notifications':get_notifications(request),
                       'trending_posts':trending_posts(), 'trending_forums':trending_forums(),
                       'followed':followed,
                        })

    # pass
class MyProfile(LoginRequiredMixin, DetailView):
    # login_url = '/login'
    # redirect_field_name = '/login'

    @login_required
    def posts(request):
        profile = request.user.profiles
        posts = Post.objects.filter(owner=request.user)
        detailed_posts = add_voted_or_not(posts, request.user)
        return render(request, 'forums/profile/comps/posts.html',
                      {'profile': profile,'trending_posts':trending_posts(), 'trending_forums':trending_forums(), 'posts': detailed_posts, 'notifications':get_notifications(request), 'notifications':get_notifications(request), 'notifications':get_notifications(request)})

    @login_required
    def comments(request):
        profile = request.user.profiles
        comments = Comment.objects.filter(owner=request.user)
        return render(request, 'forums/profile/comps/comments.html',
                      {'profile': profile,'trending_posts':trending_posts(), 'trending_forums':trending_forums(), 'comments': comments, 'notifications':get_notifications(request)})
    @login_required
    def voted_posts(request):
        profile = request.user.profiles
        voted_posts = []

        content_type = ContentType.objects.get_for_model(Post)
        votes = Vote.objects.filter(owner=request.user.id, content_type__pk=content_type.id)

        # votes = request.user.votes.all()
        for vote in votes:
            voted_posts.append(vote.content_object)
        return render(request, 'forums/profile/comps/posts.html',
                      {'profile': profile,'trending_posts':trending_posts(), 'trending_forums':trending_forums(), 'posts': voted_posts, 'notifications':get_notifications(request)})
    @login_required
    def hidden_posts(request):
        profile = request.user.profiles
        hidden_posts = Post.objects.filter(owner=request.user, hidden=True)
        return render(request, 'forums/profile/comps/posts.html',
                      {'profile': profile,'trending_posts':trending_posts(), 'trending_forums':trending_forums(), 'posts': hidden_posts, 'notifications':get_notifications(request)})

    @login_required
    def settings(request):
        profile = request.user.profiles
        hidden_posts = Post.objects.filter(owner=request.user, hidden=True)
        return render(request, 'forums/profile/comps/posts.html',
                      {'profile': profile,'trending_posts':trending_posts(), 'trending_forums':trending_forums(), 'posts': hidden_posts, 'notifications':get_notifications(request)})


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
                      {'profile': profile, 'comments': comments, 'notifications':get_notifications(request)})


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
        form.instance.owner = self.request.user
        if self.request.FILES:
            file = self.request.FILES['media_content'].name
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
            object_number = 0
            for comment in comments:
                if comment_vote[object_number] in comment.votes.all():
                    comment.voted = True
                    comment.vote_type = comment_vote[object_number].vote_type
                    comment.vote_id = comment_vote[object_number].id
                    object_number = object_number + 1

        # content_type = ContentType.objects.get_for_model(Post)
        # comments = Comment.objects.filter(content_type__pk=content_type.id)

        for comment in comments:
            content_type = ContentType.objects.get_for_model(Comment)
            children = Comment.objects.filter(content_type__pk=content_type.id, object_id=comment.id)
            comment.replies = children

        return render(request, self.template_name, {'object': post, 'comments':comments, 'notifications':get_notifications(request)})


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
    fields = ['body', 'object_id']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.content_object = Post.objects.get(id=form.instance.object_id)
        super().form_valid(form)
        return redirect('forums_post_detail', slug=form.instance.content_object.slug)

class ReplyCreateView(CreateView):
    model = Comment
    # form_class = CommentForm
    template_name = 'forums/comment/comment_form.html'
    fields = ['body', 'object_id']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.content_object = Comment.objects.get(id=form.instance.object_id)

        while True:
            instance = form.instance.content_object
            if instance.content_type.model == 'post':
                instance = instance.content_object
                break
        super().form_valid(form)
        return redirect('forums_post_detail', slug=instance.slug)


class CommentDetailView(DetailView):
    model = Comment
    template_name = 'forums/comment/comment_detail.html'


class CommentUpdateView(UpdateView):
    model = Comment
    template_name = 'forums/comment/comment_form.html'
    fields = ['body']
    # form_class = CommentForm


class VoteListView(ListView):
    model = Vote
    # template_name = 'forums/comment/comment_form.html'


class PostVoteCreateView(CreateView):
    model = Vote
    # form_class = VoteForm
    # template_name = 'forums/vote/vote_form.html'
    fields = ['vote_type', 'object_id']
    # @login_required
    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.content_object = Post.objects.get(id=form.instance.object_id)
        super().form_valid(form)
        return redirect('forums_post_detail', slug=form.instance.content_object.slug)


@login_required
def postvoteupdate(request, slug):
    if request.method == 'POST':

        post = Post.objects.get(slug = slug)
        content_type = ContentType.objects.get_for_model(Post)
        post_vote = Vote.objects.filter(owner=request.user.id, content_type__pk=content_type.id)

        vote = [value for value in post_vote.all() if value in post.votes.all()]

        vote_form = VoteForm(request.POST, instance=vote[0])
        if vote_form.is_valid():
            vote_form.save()
            print(vote_form.instance.vote_type)
            messages.success(request, f'Your account has been updated!')
            return redirect('forums_post_detail', slug=post.slug)

@login_required
def postvotedelete(request, slug):
    if request.method == 'POST':

        post = Post.objects.get(slug = slug)
        content_type = ContentType.objects.get_for_model(Post)
        post_vote = Vote.objects.filter(owner=request.user.id, content_type__pk=content_type.id)

        vote = [value for value in post_vote.all() if value in post.votes.all()][0].delete()

        return redirect('forums_post_detail', slug=post.slug)


class CommentVoteCreateView(CreateView):
    model = Vote
    # form_class = VoteForm
    fields = ['vote_type', 'object_id']
    # @login_required
    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.content_object = Comment.objects.get(id=form.instance.object_id)

        while True:
            instance = form.instance.content_object
            if instance.content_type.model == 'post':
                instance = instance.content_object
                break
        # print(form.instance.content_object.content_object.model)
        super().form_valid(form)
        return redirect('forums_post_detail', slug=instance.slug)
        # return redirect('my-profile')


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
            return reverse_lazy( 'forums_post_detail', kwargs={'slug': comment.content_object.slug})

class VoteDeleteView(DeleteView):
    model = Vote

    def get_success_url(self):
    # Assuming there is a ForeignKey from Comment to Post in your model
        if self.object.content_type.model == 'post':
            post = self.object.content_object
            return reverse_lazy( 'forums_post_detail', kwargs={'slug': post.slug})
        else:
            comment = self.object.content_object
            return reverse_lazy( 'forums_post_detail', kwargs={'slug': comment.content_object.slug})


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
        # print(request.user.is_authenticated)
        if request.user.is_authenticated:
            if request.user.is_authenticated and len(forum.forummembers.filter(member = request.user.id)) != 0:
                forum.member = forum.forummembers.get(member = request.user.id).id

            # comments = Comment.objects.filter(owner=request.user)
            common_users = [value for value in forum.forummembers.all() if value in request.user.forummembers.all()]
            if len(common_users) != 0:
                forum.followed = True
            detailed_posts = add_voted_or_not(posts, request.user)
            return render(request, self.template_name, {'forum': forum, 'posts': detailed_posts, 'notifications':get_notifications(request)})

        return render(request, self.template_name, {'forum': forum, 'posts': posts, 'notifications':get_notifications(request)})

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
