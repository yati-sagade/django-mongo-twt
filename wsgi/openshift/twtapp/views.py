from user_mgmt import follow, unfollow
from documents import UserProfile, Post
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from forms import LoginForm, SignupForm

def home(request):
    if request.user.is_authenticated():
        tpl_vars = {
            'luser': UserProfile.objects.get(username=request.user.username),
            'all_users': UserProfile.objects.all(),
            'header': 'page',
            'logged': True,
        }
        return render_to_response('twtapp/timeline.html', 
                                  RequestContext(request, tpl_vars))
        
    return render_to_response('twtapp/home_not_logged.html', 
                             RequestContext(request, {'header': 'home'})
                             )
#-------------------------------------------------------------------------------
def signup(request):
    tpl_vars = {
                'header': 'page', 
                'logged': False, 
                'signupform': SignupForm()
            }

    if request.method == 'POST':
        signupform = SignupForm(request.POST)
        if signupform.is_valid():
            cd = signupform.cleaned_data
            username, password = cd['username'], cd['password']
            if not UserProfile.find(username):
                user = UserProfile.objects.create(username=username,
                                           email='{0}@djangomongotwt.com'
                                                 .format(username))
                user.set_password(password)
                return login_view(request)

            signupform.errors['username'] = ['Oops! That id seems to be taken!']

        tpl_vars['signupform'] = signupform
    return render_to_response('twtapp/login.html',
                              RequestContext(request, tpl_vars))
#-------------------------------------------------------------------------------

def login_view(request, next_page=None):
    tpl_vars = {'header': 'page', 'logged': False, 'signupform': SignupForm()}

    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        tpl_vars['loginform'] = loginform

        if loginform.is_valid():
            cd = loginform.cleaned_data
            username, password = cd['username'], cd['password']
            
            user = UserProfile.find(username)
            if user:
                if user.check_password(password):
                    user.backend = 'mongoengine.django.auth.MongoEngineBackend'
                    login(request, user)
                    if next_page:
                        return redirect(next_page)
                
                    return redirect('/')

            loginform.errors['username'] = ['invalid username/password']
            return render_to_response('twtapp/login.html',
                                      RequestContext(request, tpl_vars))
        
        # Invalid form data
        return render_to_response('twtapp/login.html', 
                                  RequestContext(request, tpl_vars))

    # We don't have a POST(so, it's most probably, a GET!)
    if request.GET.get('next', None):
        tpl_vars['hidden_next'] = request.GET['next']

    tpl_vars['loginform'] = LoginForm()
    return render_to_response('twtapp/login.html',
                              RequestContext(request, tpl_vars))
#-------------------------------------------------------------------------------
# MongoEngine can make use of the login_required decorator from Django's auth!
@login_required
def post(request):
    '''The view that makes the tweet happen!'''
    if request.method == 'POST':
        user = UserProfile.get_user_by_id(request.user.username)
        if request.POST.get('content', None):
            tweet = user.add_post(request.POST['content'])
            user.add_to_timeline(tweet)
            # Now let the followers know
            for follower in user.get_followers():
                follower.add_to_timeline(tweet)

    return redirect('/home/')
#-------------------------------------------------------------------------------
@login_required
def logout_view(request):
    logout(request)
    return redirect('/')
#-------------------------------------------------------------------------------
def user_page(request, username):
    ruser = UserProfile.objects.get(username=username)
    luser = UserProfile.objects.get(username=request.user.username)
    tpl_vars = {
            'luser': luser,
            'ruser': ruser,
            'all_users': UserProfile.objects.all(),
            'header': 'page',
            'logged': luser.is_authenticated(),
            'himself': (luser.is_authenticated()
                        and luser.username == ruser.username),
            'is_following': (ruser.username in luser.followee),
        }

    return render_to_response('twtapp/user.html',
                              RequestContext(request,tpl_vars))
#-------------------------------------------------------------------------------
def status(request, username, tweet_id):
    try:
        tweet = Post.get_post_by_id(tweet_id)
        ruser = UserProfile.get_user_by_id(username)
    except:
        raise Http404
    
    luser = UserProfile.get_user_by_id(request.user.username)
    tpl_vars = {
            'luser': luser,
            'ruser': ruser,
            'all_users': UserProfile.objects.all(),
            'header': 'page',
            'logged': luser.is_authenticated(),
            'tweet': tweet
        }
    return render_to_response('twtapp/single.html',
                             RequestContext(request, tpl_vars))
#-------------------------------------------------------------------------------
@login_required
def follow_view(request, to_follow):
    print(request.method)
    if request.method == 'POST':
        luser = UserProfile.get_user_by_id(request.user.username)
        try:
            ruser = UserProfile.get_user_by_id(to_follow)
        except UserProfile.DoesNotExist:
            raise Http404

        follow(follower=luser, followee=ruser)
        return redirect('/%s/' % to_follow)
#-------------------------------------------------------------------------------
@login_required
def unfollow_view(request, the_creep):
    if request.method == 'POST':
        luser = UserProfile.get_user_by_id(request.user.username)
        try:
            ruser = UserProfile.get_user_by_id(the_creep)
        except UserProfile.DoesNotExist:
            raise Http404

        unfollow(follower=luser, followee=ruser)
        return redirect('/%s/' % the_creep)
#-------------------------------------------------------------------------------





            


