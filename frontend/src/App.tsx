import { useEffect } from 'react'
import { Routes, Route, useLocation } from 'react-router-dom'
import { Layout } from 'antd'
import HomePage from './pages/HomePage'
import ProjectDetailPage from './pages/ProjectDetailPage'
import SettingsPage from './pages/SettingsPage'
import Header from './components/Header'
import { trackPageview } from './analytics/posthog'

const { Content } = Layout

// Manually report pageview under HashRouter (auto pageview is disabled at init)
function usePageviewTracking() {
  const location = useLocation()
  useEffect(() => {
    trackPageview(location.pathname + location.search)
  }, [location.pathname, location.search])
}

function App() {
  console.log('App component loaded');
  usePageviewTracking()

  return (
    <Layout>
      <Header />
      <Content>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/project/:id" element={<ProjectDetailPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </Content>
    </Layout>
  )
}

export default App
