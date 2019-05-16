# encoding: utf-8

from django.views.generic.edit import CreateView, UpdateView
from django.db import models


class BaseCreateView(CreateView):
    def get_context_data(self, **kwargs):
        context = super(BaseCreateView, self).get_context_data(**kwargs)
        context.update(self.kwargs)
        return context


class BaseUpdateView(UpdateView):
    def get_context_data(self, **kwargs):
        context = super(BaseUpdateView, self).get_context_data(**kwargs)
        context.update(self.kwargs)
        return context


class BaseManager(models.Manager):
    _cache = {}

    def get_from_cache(self, key):
        return self.__class__._cache[self.db][key]

    def clear_cache(self):
        """
        Clear out the content-type cache. This needs to happen during database
        flushes to prevent caching of "stale" content type IDs (see
        django.contrib.contenttypes.management.update_contenttypes for where
        this gets called).
        """
        self.__class__._cache.clear()

    def clear_cache_by_key(self, key):
        """
        Clear out the content-type cache. This needs to happen during database
        flushes to prevent caching of "stale" content type IDs (see
        django.contrib.contenttypes.management.update_contenttypes for where
        this gets called).
        """
        d = self.__class__._cache.setdefault(self.db, {})
        if key in d[self.db]:
            del d[key]

    def add_to_cache(self, key, obj):
        self.__class__._cache.setdefault(self.db, {})[key] = obj