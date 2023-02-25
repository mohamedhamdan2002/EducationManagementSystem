from django.shortcuts import redirect

def admin_only(view_func):
    def wrapper_func(request,*args,**kwargs):
        group=None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
        
        # print('groups: ',request.user.groups.all())
        # print('usergroup',group)

        if group == 'students':
            return redirect('pages:home')
        if group == 'staff':
            return view_func(request,*args,**kwargs)
    return wrapper_func
