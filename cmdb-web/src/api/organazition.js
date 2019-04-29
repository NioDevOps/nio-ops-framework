import request from '@/utils/request'

export function getdepartmentTree(data) {
  return request({
    url: '/api/department/tree',
    method: 'get',
    data
  })
}
