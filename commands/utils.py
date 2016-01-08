# -*- coding: utf-8 -*-
""" Shared command utilities
"""
import click


def include(function_list):
    """Decorator to add command to a command container.

    :param function_list: list or mutable list-like object
    :returns: decorator
    """
    def actual_decorator(function):
        function_list.append(function)
        return function
    return actual_decorator


def write(text, nl=True, err=False, *args, **kwargs):
    if args or kwargs:
        click.echo(click.style(text, *args, **kwargs), nl=nl, err=err)
    else:
        click.echo(text, nl=nl, err=err)
