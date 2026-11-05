import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '@/services/api'

export interface AuthUser {
  is_authenticated: boolean
  id?: number
  email?: string
  first_name?: string
  last_name?: string
  full_name?: string
  status?: 'pending' | 'approved' | 'rejected' | null
  is_approved?: boolean
  is_director?: boolean
  is_site_admin?: boolean
  is_team_leader?: boolean
  member_type?: 'permanent' | 'associate' | null
  profile_slug?: string | null
}

export function useAuth() {
  const queryClient = useQueryClient()

  const { data: user, isLoading } = useQuery<AuthUser>({
    queryKey: ['auth', 'me'],
    queryFn: async () => {
      const response = await api.get<AuthUser>('/auth/me/')
      return response.data
    },
    staleTime: 1000 * 60 * 2, // 2 minutes
    retry: false,
  })

  const logoutMutation = useMutation({
    mutationFn: async () => {
      await api.post('/auth/logout/')
    },
    onSuccess: () => {
      queryClient.setQueryData(['auth', 'me'], { is_authenticated: false })
      window.location.href = '/'
    },
  })

  return {
    user: user ?? { is_authenticated: false },
    isLoading,
    isAuthenticated: Boolean(user?.is_authenticated),
    isPending: user?.status === 'pending',
    isApproved: Boolean(user?.is_approved),
    isDirector: Boolean(user?.is_director),
    isSiteAdmin: Boolean(user?.is_site_admin),
    isTeamLeader: Boolean(user?.is_team_leader),
    logout: logoutMutation.mutate,
    isLoggingOut: logoutMutation.isPending,
  }
}

export default useAuth
