import React from 'react'
import { Card, Tag, Space, Typography } from 'antd'
import { BILIBILI_PARTITIONS } from '../services/uploadApi'

const { Text } = Typography

interface UploadToBilibiliProps {
  partitionId?: number
}

const UploadToBilibili: React.FC<UploadToBilibiliProps> = ({ partitionId }) => {
  // fetchPartitionEN
  const getPartitionName = (id: number) => {
    const partition = BILIBILI_PARTITIONS.find(p => p.id === id)
    return partition ? partition.name : 'unknownPartition'
  }

  return (
    <Card
      title={
        <Space>
          <span>BENPartitioninfo</span>
          {partitionId && (
            <Tag color="blue">ENPartition: {getPartitionName(partitionId)}</Tag>
          )}
        </Space>
      }
      size="small"
      style={{ marginBottom: '16px' }}
    >
      <div>
        <Text type="secondary">
          ENPartitionEN：animation、gaming、music、knowledge、entertainment、Film & TV、TechEN
        </Text>
        <div style={{ marginTop: '12px' }}>
          <Text strong>PartitionID: </Text>
          <Text code>{partitionId || 'ENsettings'}</Text>
        </div>
      </div>
    </Card>
  )
}

export default UploadToBilibili

