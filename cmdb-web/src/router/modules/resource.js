/** When your routing table is too long, you can split it into small modules**/

import Layout from '@/views/layout/Layout'

const tableRouter = {
  path: '/resource',
  component: Layout,
  name: 'Resource',
  meta: {
    title: 'Resource',
    icon: 'table'
  },
  children: [
    {
      path: 'server',
      component: () => import('@/views/resource/server'),
      name: 'Server',
      meta: { title: 'server' }
    },
    {
      path: 'k8s',
      component: () => import('@/views/resource/server'),
      name: 'K8s',
      meta: { title: 'k8s' }
    },
    {
      path: 'db',
      component: () => import('@/views/resource/server'),
      name: 'Db',
      meta: { title: 'db' }
    }
  ]
}
export default tableRouter
