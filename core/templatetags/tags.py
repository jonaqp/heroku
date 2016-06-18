from django import template
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template import Node

register = template.Library()


@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")


@register.simple_tag
def javascript(filename, type='text/javascript'):
    """A simple shortcut to render a ``script`` tag to a static javascript file"""
    if '?' in filename and len(filename.split('?')) is 2:
        filename, params = filename.split('?')
        return '<script type="%s" src="%s?%s"></script>' % (
            type, staticfiles_storage.url(filename), params)
    else:
        return '<script type="%s" src="%s"></script>' % (
            type, staticfiles_storage.url(filename))


@register.simple_tag
def js(filename, type='text/javascript'):
    """A simple shortcut"""
    return javascript(filename, type=type)


@register.simple_tag
def css(filename):
    """A simple shortcut to render a ``link`` tag to a static CSS file"""
    return '<link rel="stylesheet" type="text/css" href="%s" />' % staticfiles_storage.url(
            filename)


@register.simple_tag
def app_css(app_name, file_path, *args, **kwargs):
    """
    A simple shortcut to render a ``link`` tag to a django app related css file
    {% app_css 'customer' 'edit-page.css' %}
    """

    path = '{version}/{app_name}/css/{file_path}'.format(
            version=settings.TEMPLATE_NAME,
            app_name=app_name,
            file_path=file_path
    )

    return css(path)


@register.simple_tag
def app_js(app_name, file_path, *args, **kwargs):
    """
    A simple shortcut to render a ``script`` tag to a django app related js file
    {% app_js 'customer' 'edit-page.js' %}
    """

    path = '{version}/{app_name}/js/{file_path}'.format(
            version=settings.TEMPLATE_NAME,
            app_name=app_name,
            file_path=file_path
    )

    return js(path)


# http://kuttler.eu/code/django-almost-spaceless-template-tag/
class AlmostSpacelessNode(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        return self.remove_whitespace(self.nodelist.render(context).strip())

    def remove_whitespace(self, value):
        value = re.sub(r'\n', ' ', value)
        value = re.sub(r'\s+', ' ', value)
        return value


@register.tag(name='almostspaceless')
def spaceless(parser, token):
    """
    Remove all whitespace except for one space from content
    """
    nodelist = parser.parse(('endalmostspaceless',))
    parser.delete_first_token()
    return AlmostSpacelessNode(nodelist)
