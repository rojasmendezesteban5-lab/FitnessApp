from django import template


register = template.Library()


@register.filter
def get_item(diccionario, clave):

    if diccionario is None:
        return None

    return diccionario.get(clave)
