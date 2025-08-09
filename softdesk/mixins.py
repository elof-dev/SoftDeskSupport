from rest_framework.exceptions import ValidationError

class ParentLookupMixin:
    """
    Mixin pour :
      - Filtrer le queryset sur un paramètre d’URL
      - Injecter ce paramètre dans le contexte du serializer
      - Assigner le parent à la création
    Attributs à configurer dans la ViewSet :
      url_param_name     => nom du paramètre GET (ex : 'project' ou 'issue')
      filter_field_name  => champ du modèle à filtrer (ex : 'project_id', 'issue_id')
      parent_model       => le modèle parent (Project ou Issue)
      parent_attribute   => nom de l’argument à passer à serializer.save()
    """
    url_param_name = None
    filter_field_name = None
    parent_model = None
    parent_attribute = None

    def get_queryset(self):
        queryset = super().get_queryset()
        value = self.request.query_params.get(self.url_param_name)
        if value and self.filter_field_name:
            queryset = queryset.filter(**{self.filter_field_name: value})
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context[self.url_param_name] = self.request.query_params.get(self.url_param_name)
        return context

    def perform_create(self, serializer):
        kwargs = {}
        value = self.request.query_params.get(self.url_param_name)
        if not value:
            raise ValidationError({self.url_param_name: f"Le paramètre '{self.url_param_name}' dans l'URL est obligatoire."})
        if self.parent_model and self.parent_attribute:
            try:
                parent = self.parent_model.objects.get(pk=value)
            except self.parent_model.DoesNotExist:
                raise ValidationError({self.url_param_name: f"{self.parent_model.__name__} inexistant."})
            kwargs[self.parent_attribute] = parent
        serializer.save(author=self.request.user, **kwargs)