import React, { useState } from 'react'
import { Modal, Steps, Card, Typography, Alert, Button, Space, Divider } from 'antd'
import { QuestionCircleOutlined, CopyOutlined, CheckOutlined } from '@ant-design/icons'

const { Paragraph, Text } = Typography
const { Step } = Steps

interface CookieHelperProps {
  visible: boolean
  onClose: () => void
}

const CookieHelper: React.FC<CookieHelperProps> = ({ visible, onClose }) => {
  const [currentStep, setCurrentStep] = useState(0)
  const [copied, setCopied] = useState(false)

  const steps = [
    {
      title: 'Sign in to Bilibili',
      description: 'Sign in to your Bilibili account in the browser',
      content: (
        <div>
          <Alert
            message="Step 1: Sign in to Bilibili"
            description="Make sure you are successfully signed in to Bilibili in your browser"
            type="info"
            showIcon
            style={{ marginBottom: 16 }}
          />
          <Card size="small">
            <Paragraph>
              1. Open your browser and visit <Text code>https://www.bilibili.com</Text>
            </Paragraph>
            <Paragraph>
              2. Click the "Sign in" button at the top-right
            </Paragraph>
            <Paragraph>
              3. Sign in with your Bilibili account
            </Paragraph>
            <Paragraph>
              4. After signing in, you should see your username at the top-right
            </Paragraph>
          </Card>
        </div>
      )
    },
    {
      title: 'Open devtools',
      description: 'Press F12 to open browser devtools',
      content: (
        <div>
          <Alert
            message="Step 2: Open devtools"
            description="Use the shortcut to open browser devtools"
            type="info"
            showIcon
            style={{ marginBottom: 16 }}
          />
          <Card size="small">
            <Paragraph>
              <Text strong>Windows/Linux:</Text> press <Text code>F12</Text>
            </Paragraph>
            <Paragraph>
              <Text strong>Mac:</Text> press <Text code>Command + Option + I</Text>
            </Paragraph>
            <Paragraph>
              Or right-click an empty area and choose "Inspect"
            </Paragraph>
            <Divider />
            <Paragraph type="secondary">
              Devtools will open at the bottom or side, with several tabs
            </Paragraph>
          </Card>
        </div>
      )
    },
    {
      title: 'Switch to Network tab',
      description: 'Find the Network tab',
      content: (
        <div>
          <Alert
            message="Step 3: Switch to the Network tab"
            description="Find the Network tab in devtools"
            type="info"
            showIcon
            style={{ marginBottom: 16 }}
          />
          <Card size="small">
            <Paragraph>
              1. Find the tabs at the top of devtools
            </Paragraph>
            <Paragraph>
              2. Click the <Text code>Network</Text> tab
            </Paragraph>
            <Paragraph>
              3. Make sure the Network panel is empty (clear it if not)
            </Paragraph>
            <Divider />
            <Paragraph type="secondary">
              The Network tab monitors network requests, including cookies
            </Paragraph>
          </Card>
        </div>
      )
    },
    {
      title: 'Refresh the page',
      description: 'Refresh Bilibili to capture requests',
      content: (
        <div>
          <Alert
            message="Step 4: Refresh the page"
            description="Refresh Bilibili to capture network requests"
            type="info"
            showIcon
            style={{ marginBottom: 16 }}
          />
          <Card size="small">
            <Paragraph>
              1. Make sure the Network tab is open
            </Paragraph>
            <Paragraph>
              2. Press <Text code>F5</Text> or click the browser refresh button
            </Paragraph>
            <Paragraph>
              3. Watch the request list appear in the Network panel
            </Paragraph>
            <Divider />
            <Paragraph type="secondary">
              After refreshing, the Network panel shows all requests during page load
            </Paragraph>
          </Card>
        </div>
      )
    },
    {
      title: 'Find the cookie',
      description: 'Find the Cookie in request headers',
      content: (
        <div>
          <Alert
            message="Step 5: Find the cookie"
            description="Find the Cookie field in any request"
            type="info"
            showIcon
            style={{ marginBottom: 16 }}
          />
          <Card size="small">
            <Paragraph>
              1. Pick any request in the Network panel (usually the first)
            </Paragraph>
            <Paragraph>
              2. Click it and find the <Text code>Headers</Text> tab on the right
            </Paragraph>
            <Paragraph>
              3. In <Text code>Request Headers</Text> find the <Text code>Cookie</Text> field
            </Paragraph>
            <Paragraph>
              4. Its value is the full cookie string you need
            </Paragraph>
            <Divider />
            <Paragraph type="secondary">
              The cookie string is usually long, with multiple key-value pairs separated by semicolons
            </Paragraph>
          </Card>
        </div>
      )
    },
    {
      title: 'Copy the cookie',
      description: 'Copy the full cookie string',
      content: (
        <div>
          <Alert
            message="Step 6: Copy the cookie"
            description="Copy the full cookie string to the clipboard"
            type="success"
            showIcon
            style={{ marginBottom: 16 }}
          />
          <Card size="small">
            <Paragraph>
              1. Right-click the cookie value
            </Paragraph>
            <Paragraph>
              2. Choose "Copy value"
            </Paragraph>
            <Paragraph>
              3. Or double-click to select the whole value, then press <Text code>Ctrl+C</Text>
            </Paragraph>
            <Divider />
            <Paragraph type="secondary">
              You can paste the copied cookie directly into AutoClip's cookie input
            </Paragraph>
            <Alert
              message="Important"
              description="The cookie contains your sign-in info — keep it safe and don't share it"
              type="warning"
              showIcon
            />
          </Card>
        </div>
      )
    }
  ]

  const handleCopy = () => {
    const cookieExample = "SESSDATA=your_sessdata_here; bili_jct=your_bili_jct_here; DedeUserID=your_dedeuserid_here"
    navigator.clipboard.writeText(cookieExample).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    })
  }

  return (
    <Modal
      title={
        <Space>
          <QuestionCircleOutlined />
          <span>Cookie guide</span>
        </Space>
      }
      open={visible}
      onCancel={onClose}
      footer={[
        <Button key="back" onClick={onClose}>
          Close
        </Button>,
        <Button
          key="copy"
          icon={copied ? <CheckOutlined /> : <CopyOutlined />}
          onClick={handleCopy}
        >
          {copied ? 'Copied' : 'Copy example'}
        </Button>
      ]}
      width={700}
    >
      <div style={{ marginBottom: 16 }}>
        <Alert
          message="Cookie import is the safest sign-in"
          description="Compared to QR login, cookie import won't trigger Bilibili risk controls and is the most recommended."
          type="success"
          showIcon
        />
      </div>

      <Steps current={currentStep} onChange={setCurrentStep} direction="vertical" size="small">
        {steps.map((step, index) => (
          <Step key={index} title={step.title} description={step.description} />
        ))}
      </Steps>

      <div style={{ marginTop: 24, padding: 16, backgroundColor: '#f5f5f5', borderRadius: 8 }}>
        {steps[currentStep].content}
      </div>

      <Divider />

      <Card size="small" title="Cookie format example">
        <Paragraph code style={{ fontSize: '12px', wordBreak: 'break-all' }}>
          SESSDATA=your_sessdata_here; bili_jct=your_bili_jct_here; DedeUserID=your_dedeuserid_here; buvid3=your_buvid3_here
        </Paragraph>
        <Paragraph type="secondary" style={{ fontSize: '12px' }}>
          Note: a real cookie is much longer with more fields
        </Paragraph>
      </Card>
    </Modal>
  )
}

export default CookieHelper
