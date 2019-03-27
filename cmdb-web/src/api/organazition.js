import request from '@/utils/request'

export function getdepartmentTree(data) {
  return request({
    url: '/api/departments/tree',
    method: 'get',
    data
  })
}
