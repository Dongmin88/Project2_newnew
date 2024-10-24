# recommendations/views.py
import sys
import os
import json
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from link_image import link_image  # link_image 함수 가져오기

RECOMMENDATION_HISTORY_KEY = 'recommendation_history'

def recommend(request, category):
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')

    recommendation_history = request.session.get(RECOMMENDATION_HISTORY_KEY, {})
    if category not in recommendation_history:
        recommendation_history[category] = []

    recommendations = get_recommendations(category,latitude,longitude,recommendation_history[category])
    
    recommendation_history[category].append(recommendations['name'])
    request.session[RECOMMENDATION_HISTORY_KEY] = recommendation_history

    # 이미지 경로 가져오기
    image_path = link_image(recommendations['name'])

    # AJAX 요청인지 확인
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # AJAX 요청일 경우 HTML만 반환
        html = render_to_string('recommendations/recommend_content.html', {
            'recommendations': recommendations,
            'image_path': image_path  # 이미지 경로 전달
        })
        return JsonResponse({'html': html})

    # 일반 요청일 경우 전체 페이지 렌더링
    return render(request, 'recommendations/recommend.html', {
        'category': category,
        'recommendations': recommendations,
        'image_path': image_path  # 이미지 경로 전달
    })

def index(request):
    return render(request, 'recommendations/index.html')

def get_recommendations(category, latitude, longitude, previous_recommendations):
    sys.stdout.reconfigure(encoding='utf-8')
    
    # 이전 추천을 제외하는 조건 추가
    exclude_condition = ""
    if previous_recommendations:
        exclude_condition = f" {', '.join(previous_recommendations)} 이름을 가진 장소들은 제외해줘."

    input_string = f"현재 나의 위치는 위도 {latitude}, 경도 {longitude}이다. 제주도에서 가까운 {category} 장소를 1개 알려줘. name은 장소이름이다. user_review는 사용자 리뷰를 보고 써달라. duration_time은 현재 나의 위치에서 자동차로 걸리는 시간이다.{exclude_condition}"

    # Azure OpenAI 설정




    completion_dict = json.loads(completion.to_json())
    content = completion_dict['choices'][0]['message']['content']
    print(content)
    content = content.replace("json", "").replace("`", "").strip()
    data = json.loads(content)
    print(data)
    # 반환된 데이터가 단일 객체이므로 리스트가 아닌 단일 객체로 반환
    return data