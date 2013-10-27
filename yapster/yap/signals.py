from django.dispatch import Signal


yap_created = Signal(providing_args=["yap", ])
yap_deleted = Signal(providing_args=["yap", ])

reyap_created = Signal(providing_args=["reyap", ])
reyap_deleted = Signal(providing_args=["reyap", ])
