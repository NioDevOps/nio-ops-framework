import request from '@/utils/request'

export function getServiceTree(data) {
  return request({
    url: '/api/service/tree',
    method: 'get',
    data
  })
}
