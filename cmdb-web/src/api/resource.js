import request from '@/utils/request'

export function getResource(data) {
  return request({
    url: '/v1/resources',
    method: 'get',
    params: data,
  })
}
