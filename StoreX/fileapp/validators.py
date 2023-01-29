from django.core.validators import FileExtensionValidator

# specifying the file extension we want to store and then importing and using it in the model FileField instance
validators = [FileExtensionValidator(allowed_extensions=['txt', 'pdf', 'docx', 'ppt', 'pptx', 'xlsx'])]