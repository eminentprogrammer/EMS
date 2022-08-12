def get_ip(request):
    ip = ""
    address = request.META.get('HTTP_X_FORWARDED_FOR')
    if address:
        ip = address.split(',')[-1].strip()
        port = request.META.get('SERVER_PORT')
    else:
        ip = request.META.get('REMOTE_ADDR')
        port = request.META.get('SERVER_PORT')
        user_domain_name = request.META.get('USERDOMAIN')
        user_domain_profile = request.META.get('USERDOMAIN_ROAMINGPROFILE')
        hostname = request.META.get('USERNAME')
        print(hostname, user_domain_name, user_domain_profile)
    host_domain = ip+":"+port
    return f"{user_domain_profile} || {host_domain}"
