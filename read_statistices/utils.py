from django.contrib.contenttypes.models import ContentType
from .models import ReadNum


def read_statics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "{}_{}_read".format(ct.model, obj.pk)

    if not request.COOKIES.get(key):
        if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
            # 存在记录
            readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        else:
            # 不存在对应记录
            readnum = ReadNum(content_type=ct, object_id=obj.pk)
        # 计数器加1
        readnum.read_num += 1
        readnum.save()
    return key