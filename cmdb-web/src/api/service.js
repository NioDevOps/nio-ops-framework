import request from '@/utils/request'

export function getServiceTree(data) {
  return request({
    url: '/api/service/tree',
    method: 'get',
    data
  })
}

export function postService(data) {
  return request({
    url: '/v1/service/',
    method: 'post',
    data
  })
}

