import React, { useState, useEffect } from 'react'
import { 
  Layout, 
  Typography, 
  Select, 
  Spin, 
  Empty,
  message 
} from 'antd'
import { useNavigate } from 'react-router-dom'
import ProjectCard from '../components/ProjectCard'
import FileUpload from '../components/FileUpload'
import BilibiliDownload from '../components/BilibiliDownload'

import { projectApi } from '../services/api'
import { useSimpleProgressStore } from '../stores/useSimpleProgressStore'
import { Project, useProjectStore } from '../store/useProjectStore'
import { useProjectPolling } from '../hooks/useProjectPolling'

const { Content } = Layout
const { Title, Text } = Typography
const { Option } = Select

const HomePage: React.FC = () => {
  const navigate = useNavigate()
  const { projects, setProjects, deleteProject, loading, setLoading } = useProjectStore()
  const [statusFilter, setStatusFilter] = useState<string>('all')
  const [activeTab, setActiveTab] = useState<'upload' | 'bilibili'>('bilibili')

  // Use project polling hook
  useProjectPolling({
    onProjectsUpdate: (updatedProjects) => {
      setProjects(updatedProjects || [])
    },
    enabled: true,
    interval: 30000 // Poll every 30s to reduce request frequency
  })

  // Global safeguard: when no project is running, force-stop progress polling and clear cache
  useEffect(() => {
    const hasActive = projects.some(p => p.status === 'processing' || p.status === 'pending')
    if (!hasActive) {
      try {
        const { stopPolling, clearAllProgress } = useSimpleProgressStore.getState()
        stopPolling()
        clearAllProgress()
        console.log('No running projects, stopped progress polling and cleared progress cache')
      } catch (e) {
        console.warn('Issue stopping global progress polling:', e)
      }
    }
  }, [projects])

  useEffect(() => {
    // Delay loading projects to avoid a burst of requests on startup
    const timer = setTimeout(() => {
      loadProjects()
    }, 1000) // Delay 1s
    
    return () => clearTimeout(timer)
  }, [])

  const loadProjects = async () => {
    setLoading(true)
    try {
      // Fetch real project data from backend API
      const projects = await projectApi.getProjects()
      // Ensure projects is an array
      const safeProjects = Array.isArray(projects) ? projects : []
      setProjects(safeProjects)
    } catch (error) {
      message.error('Failed to load projects')
      console.error('Load projects error:', error)
      // Set empty array if the API call fails
      setProjects([])
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteProject = async (id: string) => {
    try {
      await projectApi.deleteProject(id)
      deleteProject(id)
      message.success('Project deleted successfully')
    } catch (error) {
      message.error('Failed to delete project')
      console.error('Delete project error:', error)
    }
  }

  // Called by ProjectCard after the user manually clicks retry and the retry request has succeeded.
  // ProjectCard.handleRetry already sent the start/retryProcessing request; this only handles
  // messaging + list refresh and must never send another retry request (it would stack on top of
  // the card's own request and create a loadProjects -> remount -> auto-start loop).
  const handleRetryProject = async () => {
    message.success('Retrying project processing')
    try {
      await loadProjects()
    } catch (error) {
      console.error('Refresh after retry error:', error)
    }
  }

  const handleProjectCardClick = (project: Project) => {
    // Projects in pending import state cannot be opened
    if (project.status === 'pending') {
      message.warning('Project is still importing, please check details later')
      return
    }
    
    // Other states can open the detail page normally
    navigate(`/project/${project.id}`)
  }

  const filteredProjects = (projects || [])
    .filter(project => {
      const matchesStatus = statusFilter === 'all' || project.status === statusFilter
      return matchesStatus
    })
    .sort((a, b) => {
      // Sort by creation time descending, newest first
      return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    })

  return (
    <Layout style={{
      minHeight: '100vh',
      background: 'var(--ac-bg)'
    }}>
      <Content style={{ padding: '40px 56px 56px', position: 'relative' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', position: 'relative' }}>
          {/* File upload area */}
          <div style={{ 
            marginBottom: '48px',
            marginTop: '20px',
            display: 'flex',
            justifyContent: 'center'
          }}>
            <div style={{ width: '100%', maxWidth: '820px' }}>
              <div style={{ fontSize: '13px', color: 'var(--ac-muted)', margin: '0 4px 14px', letterSpacing: '0.2px' }}>
                Paste a link, AI auto-clips it
              </div>
              <div style={{
                background: 'var(--ac-card)',
                borderRadius: '16px',
                border: '1px solid var(--ac-line)',
                padding: '18px',
                boxShadow: 'var(--ac-shadow)'
              }}>
              {/* Tab switch — pill segmented */}
              <div style={{
                display: 'inline-flex',
                marginBottom: '14px',
                borderRadius: '999px',
                background: 'var(--ac-line-2)',
                padding: '3px',
                gap: '2px'
              }}>
                 <button
                   style={{
                     padding: '8px 18px',
                     borderRadius: '999px',
                     background: activeTab === 'bilibili' ? 'var(--ac-card)' : 'transparent',
                     color: activeTab === 'bilibili' ? 'var(--ac-ink)' : 'var(--ac-sub)',
                     cursor: 'pointer',
                     fontSize: '14px',
                     fontWeight: 500,
                     transition: 'all 0.2s ease',
                     border: 'none',
                     boxShadow: activeTab === 'bilibili' ? '0 1px 2px rgba(0,0,0,.08)' : 'none'
                   }}
                   onClick={() => setActiveTab('bilibili')}
                 >
                    Link import
                  </button>
                <button
                   style={{
                     padding: '8px 18px',
                     borderRadius: '999px',
                     background: activeTab === 'upload' ? 'var(--ac-card)' : 'transparent',
                     color: activeTab === 'upload' ? 'var(--ac-ink)' : 'var(--ac-sub)',
                     cursor: 'pointer',
                     fontSize: '14px',
                     fontWeight: 500,
                     transition: 'all 0.2s ease',
                     border: 'none',
                     boxShadow: activeTab === 'upload' ? '0 1px 2px rgba(0,0,0,.08)' : 'none'
                   }}
                   onClick={() => setActiveTab('upload')}
                 >
                    File import
                  </button>
              </div>
              
              {/* Content area */}
              <div>
                {activeTab === 'bilibili' && (
                  <BilibiliDownload onDownloadSuccess={async () => {
                    // Refresh the project list after processing completes
                    await loadProjects()
                    // No duplicate toast; the BilibiliDownload component already shows a unified message
                  }} />
                )}
                {activeTab === 'upload' && (
                  <FileUpload onUploadSuccess={async () => {
                    // Refresh the project list after processing completes
                    await loadProjects()
                    message.success('Project created, now processing...')
                  }} />
                )}
              </div>
              </div>
            </div>
          </div>

          {/* Project management area */}
          <div style={{
            background: 'transparent',
            padding: '0',
            marginBottom: '32px'
          }}>
            {/* Project list header */}
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'baseline',
              marginTop: '56px',
              marginBottom: '22px'
            }}>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: '12px' }}>
                <Title
                  level={2}
                  style={{ margin: 0, color: 'var(--ac-ink)', fontSize: '16px', fontWeight: 600 }}
                >
                  My Projects
                </Title>
                <Text style={{ color: 'var(--ac-muted)', fontSize: '13px' }}>
                  {filteredProjects.length}
                </Text>
              </div>
              
              {/* Status filter on the right */}
              <div style={{ 
                display: 'flex', 
                alignItems: 'center'
              }}>
                <Select
                  placeholder="All statuses"
                  value={statusFilter}
                  onChange={setStatusFilter}
                  variant="borderless"
                  style={{ minWidth: '120px', fontSize: '13px' }}
                  suffixIcon={<span style={{ color: 'var(--ac-muted)', fontSize: '10px' }}>⌄</span>}
                  allowClear
                >
                  <Option value="all">All statuses</Option>
                  <Option value="completed">Completed</Option>
                  <Option value="processing">Processing</Option>
                  <Option value="error">Failed</Option>
                </Select>
              </div>
            </div>

            {/* Project list content */}
             <div>
               {loading ? (
                 <div style={{
                   textAlign: 'center',
                   padding: '72px 0',
                   background: 'var(--ac-card)',
                   borderRadius: '16px',
                   border: '1px solid var(--ac-line)'
                 }}>
                   <Spin size="large" />
                   <div style={{ marginTop: '18px', color: 'var(--ac-muted)', fontSize: '14px' }}>
                      Loading project list...
                   </div>
                 </div>
               ) : filteredProjects.length === 0 ? (
                 <div style={{
                   textAlign: 'center',
                   padding: '72px 0',
                   background: 'var(--ac-card)',
                   borderRadius: '16px',
                   border: '1px solid var(--ac-line)'
                 }}>
                   <Empty
                     image={Empty.PRESENTED_IMAGE_SIMPLE}
                     description={
                       <div>
                         <Text type="secondary">
                            {projects.length === 0 ? 'No projects yet, use the import area above to create your first project' : 'No matching projects found'}
                         </Text>
                       </div>
                     }
                   />
                 </div>
               ) : (
                 <div style={{
                   display: 'grid',
                   gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
                   gap: '24px',
                   justifyContent: 'start'
                 }}>
                   {filteredProjects.map((project: Project) => (
                     <div key={project.id} style={{ position: 'relative', zIndex: 1 }}>
                       <ProjectCard 
                         project={project} 
                         onDelete={handleDeleteProject}
                         onRetry={() => handleRetryProject()}
                         onClick={() => handleProjectCardClick(project)}
                       />
                     </div>
                   ))}
                 </div>
               )}
             </div>
           </div>
         </div>
      </Content>
    </Layout>
  )
}

export default HomePage