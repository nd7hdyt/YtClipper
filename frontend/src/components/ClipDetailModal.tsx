import React, { useState, useRef } from 'react'
import { Modal, Typography, Button, Tag, Space, Row, Col, Divider } from 'antd'
import { 
  PlayCircleOutlined, 
  DownloadOutlined, 
  ClockCircleOutlined, 
  StarFilled,
  CloseOutlined
} from '@ant-design/icons'
import ReactPlayer from 'react-player'
import { Clip } from '../store/useProjectStore'
import { projectApi } from '../services/api'
import EditableTitle from './EditableTitle'

const { Text, Title } = Typography

interface ClipDetailModalProps {
  visible: boolean
  clip: Clip | null
  projectId: string
  onClose: () => void
  onDownload: (clipId: string) => void
}

const ClipDetailModal: React.FC<ClipDetailModalProps> = ({
  visible,
  clip,
  projectId,
  onClose,
  onDownload
}) => {
  const [playing, setPlaying] = useState(false)
  const [downloading, setDownloading] = useState(false)
  const playerRef = useRef<ReactPlayer>(null)

  const formatTime = (timeStr: string) => {
    if (!timeStr) return '00:00:00'
    // translated'stranslatedsecondstranslated，translatedseconds
    return timeStr.replace(',', '.').substring(0, 8)
  }

  const getDuration = () => {
    if (!clip?.start_time || !clip?.end_time) return '00:00:00'
    const start = clip.start_time.replace(',', '.')
    const end = clip.end_time.replace(',', '.')
    return `${start.substring(0, 8)} - ${end.substring(0, 8)}`
  }

  const getScoreColor = (score: number) => {
    // translatedsettingstranslated'stranslated
    if (score >= 0.9) return '#52c41a' // translated - translated
    if (score >= 0.8) return '#1890ff' // translated - translated
    if (score >= 0.7) return '#faad14' // translated - onetranslated
    if (score >= 0.6) return '#ff7a45' // translated - translated
    return '#ff4d4f' // translated - translated
  }

  const handleDownload = async () => {
    if (!clip) return
    setDownloading(true)
    try {
      await onDownload(clip.id)
    } finally {
      setDownloading(false)
    }
  }

  const handleClose = () => {
    setPlaying(false)
    onClose()
  }

  if (!clip) return null

  return (
    <>
      <Modal
        visible={visible}
        onCancel={handleClose}
        footer={null}
        width={800}
        centered
        destroyOnClose
        style={{ top: 20 }}
        styles={{
          body: {
            padding: 0,
            background: 'rgba(26, 26, 46, 0.95)',
            borderRadius: '12px'
          }
        }}
      >
        <div style={{ padding: '24px' }}>
          {/* translated */}
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            marginBottom: '20px'
          }}>
            <Title level={4} style={{ margin: 0, color: '#ffffff' }}>
              cliptranslated
            </Title>
            <Button 
              type="text" 
              icon={<CloseOutlined />} 
              onClick={handleClose}
              style={{ color: '#cccccc' }}
            />
          </div>

          <Row gutter={24}>
            {/* translatedvideotranslated */}
            <Col span={14}>
              <div style={{ 
                background: '#000', 
                borderRadius: '8px', 
                overflow: 'hidden',
                marginBottom: '16px'
              }}>
                <ReactPlayer
                  ref={playerRef}
                  url={projectApi.getClipVideoUrl(projectId, clip.id, clip.title || clip.generated_title)}
                  width="100%"
                  height="300px"
                  playing={playing}
                  controls
                  onPlay={() => setPlaying(true)}
                  onPause={() => setPlaying(false)}
                  style={{ borderRadius: '8px' }}
                />
              </div>

              {/* videoinfo */}
              <div style={{ marginBottom: '16px' }}>
                <Space size="middle">
                  <Tag color="blue" icon={<ClockCircleOutlined />}>
                    {getDuration()}
                  </Tag>
                  {clip.final_score && (
                    <Tag 
                      icon={<StarFilled />}
                      style={{ 
                        background: getScoreColor(clip.final_score),
                        color: 'white',
                        border: 'none'
                      }}
                    >
                      translated: {(clip.final_score * 100).toFixed(0)}translated
                    </Tag>
                  )}
                  {clip.outline && (
                    <Tag color="purple">{clip.outline}</Tag>
                  )}
                </Space>
              </div>

              {/* translatedbytranslated */}
              <Space>
                <Button 
                  type="primary" 
                  icon={<PlayCircleOutlined />}
                  onClick={() => setPlaying(!playing)}
                >
                  {playing ? 'translated' : 'translated'}
                </Button>
                <Button 
                  type="default" 
                  icon={<DownloadOutlined />}
                  loading={downloading}
                  onClick={handleDownload}
                >
                  downloadclip
                </Button>
              </Space>
            </Col>

            {/* translatedinfo */}
            <Col span={10}>
              <div style={{ color: '#ffffff' }}>
                {/* translated */}
                <div style={{ marginBottom: '16px' }}>
                  <div style={{ marginBottom: '8px' }}>
                    <EditableTitle
                      title={clip.generated_title || clip.title || 'translated'}
                      clipId={clip.id}
                      onTitleUpdate={(newTitle) => {
                        // updateclip'stranslated
                        console.log('translatedupdate:', newTitle)
                        // thistranslatedcantranslated'supdatetranslated
                      }}
                      style={{ color: '#ffffff', fontSize: '18px', fontWeight: '600' }}
                    />
                  </div>
                  <Text style={{ color: '#cccccc', fontSize: '12px' }}>
                    ID: {clip.id}
                  </Text>
                </div>

                <Divider style={{ borderColor: 'rgba(255,255,255,0.1)' }} />

                {/* translated */}
                {clip.content && clip.content.length > 0 && (
                  <div style={{ marginBottom: '16px' }}>
                    <Text strong style={{ color: '#ffffff', display: 'block', marginBottom: '8px' }}>
                      translated:
                    </Text>
                    <div>
                      {clip.content.map((point, index) => (
                        <div key={index} style={{ 
                          color: '#cccccc', 
                          fontSize: '14px',
                          marginBottom: '4px',
                          padding: '4px 8px',
                          background: 'rgba(255,255,255,0.05)',
                          borderRadius: '4px'
                        }}>
                          • {point}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* translatedinfo */}
                <div style={{ marginBottom: '16px' }}>
                  <Text strong style={{ color: '#ffffff', display: 'block', marginBottom: '8px' }}>
                    translatedinfo:
                  </Text>
                  <div style={{ color: '#cccccc', fontSize: '14px' }}>
                    <div>translated: {formatTime(clip.start_time)}</div>
                    <div>translated: {formatTime(clip.end_time)}</div>
                  </div>
                </div>


              </div>
            </Col>
          </Row>
        </div>
      </Modal>
    </>
  )
}

export default ClipDetailModal 