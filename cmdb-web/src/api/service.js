import request from '@/utils/request'

export function getServiceTree(data) {
  return request({
    url: '/api/service/tree',
    method: 'get',
    data
  })
}

export function postNormalService(data) {
  return request({
    url: '/v1/normal-service/',
    method: 'post',
    data
  })
}

