import { message } from 'antd'

export async function validateApiConfigBeforeProjectCreation(): Promise<boolean> {
  try {
    return true
  } catch (error) {
    console.error('APIconfigcheckFailed:', error)
    message.error('APIconfigcheckFailed')
    return false
  }
}
