import json

from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from django.core.exceptions import ObjectDoesNotExist

from .models import Item, Review

REVIEW_SCHEMA = {
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
        'title': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 64,
        },
        'description': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 1024,
        },
        'price': {
            'type': 'integer',
            'minimum': 1,
            'maximum': 1000000,
        },
    },
    'required': ['title', 'description', 'price'],
}

REVIEW_SCHEMA_DESCRIPTION = {
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
        'text': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 1024,
        },
        'grade': {
            'type': 'integer',
            'minimum': 1,
            'maximum': 10,
        },
    },
    'required': ['text', 'grade'],
}


@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            validate(data, REVIEW_SCHEMA)
            item = Item(**data)
            item.save()

            # from pdb import set_trace; set_trace()
        except (json.JSONDecodeError, ValidationError, AssertionError):
            return HttpResponse(status=400)

        return JsonResponse({"id": item.pk}, status=201)

@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(View):

    def post(self, request, item_id):
        try:
            data = json.loads(request.body)
            validate(data, REVIEW_SCHEMA_DESCRIPTION)
            item = Item.objects.get(pk=item_id)

            review = Review(**data)
            review.item = item
            review.save()
        except Item.DoesNotExist:
            return HttpResponse(status=404)
        except (json.JSONDecodeError, ValidationError):
            return HttpResponse(status=400)

        return JsonResponse({id: item.pk}, status=201)


class GetItemView(View):

    def get(self, request, item_id):
        # try:
        #     result = get_item_by_id(item_id)
        #     data = dict()
        #
        #     for rec in result:
        #         if not data:
        #             dict['id'] = rec.id
        #             dict['title'] = rec.title
        #             dict['description'] = rec.description
        #             dict['price'] = rec.price
        #             dict['reviews'] = []
        #         dict['reviews'].append({
        #             'id': rec.id,
        #             'text': rec.text,
        #             'grade': rec.grade,
        #         })
        #     # from pdb import set_trace; set_trace()
        #
        #     return JsonResponse(data, status=200)
        # except  ObjectDoesNotExist:
        #     return JsonResponse({}, status=404)

        try:
            item = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            return HttpResponse(status=404)
        data = list(item.values())
        query = Review.objects.filter(item=item).order_by('-id')
        reviews = query[:5]
        data['reviews'] = list(reviews.values())

        return JsonResponse(data, status=200)


def get_item_by_id(item_id):
    return Item.objects.filter(review__id=item_id)[:5] \
        .values('id', 'title', 'description', 'price', 'review__id', 'review__text', 'review__grade')
