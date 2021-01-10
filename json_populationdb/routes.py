def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/')
    config.add_route('persons', '/services/persons')        
    config.add_route('person', '/services/person/{code}')
    config.add_route('photo', '/services/person/{code}/photo')
