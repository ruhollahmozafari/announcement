from django.contrib import admin
from django.apps import apps

# Get all the models in the app
app = apps.get_app_config("user")
models = app.get_models()

exclude_fields_display = ["password"]

# Dynamically generate admin configuration for each model
for model in models:
    # Create a new admin class for the model
    admin_class = type(
        "DynamicAdmin",
        (admin.ModelAdmin,),
        {
            "list_display": [
                field.name
                for field in model._meta.fields
                if field.name not in exclude_fields_display
            ],
            "search_fields": [field.name for field in model._meta.fields if field.name not in exclude_fields_display],
        },
    )

    # Register the model with the dynamically created admin class
    admin.site.register(model, admin_class)
