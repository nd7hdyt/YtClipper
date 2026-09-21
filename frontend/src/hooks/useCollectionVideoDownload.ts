import { useState } from 'react'
import { message } from 'antd'
import { projectApi } from '../services/api'

export const useCollectionVideoDownload = () => {
  const [isGenerating, setIsGenerating] = useState(false)

  const generateAndDownloadCollectionVideo = async (
    projectId: string, 
    collectionId: string,
    _collectionTitle: string
  ) => {
    if (isGenerating) return

    setIsGenerating(true)
    
    try {
      // ENOrdergenerateCollectionvideo
      message.info('ENOrdergenerateCollectionvideo...')
      
      // generateCollectionvideo（ENOrder）
      await projectApi.generateCollectionVideo(projectId, collectionId)
      
      // waiting1ENCompletedENgenerate，ENdownload
      message.success('CollectionvideogenerateSucceeded，ENdownload...')
      
      setTimeout(async () => {
        try {
          await projectApi.downloadVideo(projectId, undefined, collectionId)
          message.success('CollectionvideodownloadCompleted')
        } catch (downloadError) {
          console.error('Download failed:', downloadError)
          message.error('Download failed，ENRetry')
        }
      }, 1000)
      
    } catch (error) {
      console.error('generateCollectionvideoFailed:', error)
      message.error('generateCollectionvideoFailed')
    } finally {
      setIsGenerating(false)
    }
  }

  return {
    isGenerating,
    generateAndDownloadCollectionVideo
  }
} 