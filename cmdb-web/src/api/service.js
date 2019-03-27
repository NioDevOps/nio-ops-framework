import request from '@/utils/request'

export function getServiceTree(data) {
  return request({
    url: '/api/services/tree',
    method: 'get',
    data
  })
}
