import React, { useState, useEffect } from 'react';
import { useWebSocket, WebSocketEventMessage } from '../hooks/useWebSocket';

interface InlineProgressBarProps {
  projectId: string;
  currentStep?: number;
  totalSteps?: number;
  status?: string;
  onProgressUpdate?: (progress: number, step: string) => void;
}

interface ProgressData {
  progress: number;
  currentStep: number;
  totalSteps: number;
  stepName: string;
  stepDetails?: string;
}

// Pipeline step config
const PIPELINE_STEPS = [
  { id: 1, name: 'Outline extraction', description: 'Extract a structured outline from the transcript' },
  { id: 2, name: 'Time locating', description: 'Locate topic ranges using SRT subtitles' },
  { id: 3, name: 'Content scoring', description: 'Score clips on quality and viral potential' },
  { id: 4, name: 'Title generation', description: 'Generate catchy titles for top clips' },
  { id: 5, name: 'Topic clustering', description: 'Group related clips into collection picks' },
  { id: 6, name: 'Video cutting', description: 'Render clips and collections with FFmpeg' }
];

export const InlineProgressBar: React.FC<InlineProgressBarProps> = ({
  projectId,
  currentStep = 0,
  totalSteps = 6,
  status = 'processing',
  onProgressUpdate
}) => {
  // Step name by ID
  const getStepName = (stepId: number): string => {
    const step = PIPELINE_STEPS.find(s => s.id === stepId);
    return step ? step.name : 'Processing...';
  };

  const [progressData, setProgressData] = useState<ProgressData>({
    progress: currentStep > 0 ? Math.round((currentStep / totalSteps) * 100) : 0,
    currentStep: currentStep,
    totalSteps: totalSteps,
    stepName: currentStep > 0 ? getStepName(currentStep) : 'Initializing...',
    stepDetails: ''
  });

  // WebSocket for live progress updates
  const { isConnected, syncSubscriptions } = useWebSocket({
    userId: `homepage-user`, // Single shared user ID to avoid duplicate connections
    onMessage: (message: WebSocketEventMessage) => {
      console.log('InlineProgressBar got WebSocket message:', message);
      if (message.type === 'task_progress_update' && 
          message.project_id === projectId) {
        handleProgressUpdate(message);
      }
    }
  });

  // Handle progress updates
  const handleProgressUpdate = (message: any) => {
    console.log('InlineProgressBar handling progress update:', message);
    
    const newProgress = message.progress || 0;
    const stepName = message.step_name || 'Processing...';
    const stepDetails = message.message || '';
    
    // Snapshot guard - avoid going backwards
    if (message.snapshot && progressData.progress > newProgress) {
      console.log('Ignoring stale snapshot:', { current: progressData.progress, snapshot: newProgress });
      return;
    }
    
    console.log('Updating progress data:', { newProgress, stepName, stepDetails });
    
    setProgressData(prev => ({
      ...prev,
      progress: newProgress,
      stepName: stepName,
      stepDetails: stepDetails
    }));

    // Notify parent
    onProgressUpdate?.(newProgress, stepName);
  };

  // Sync on prop changes
  useEffect(() => {
    const newProgress = currentStep > 0 ? Math.round((currentStep / totalSteps) * 100) : 0;
    const newStepName = currentStep > 0 ? getStepName(currentStep) : 'Initializing...';
    
    setProgressData(prev => ({
      ...prev,
      progress: newProgress,
      currentStep: currentStep,
      totalSteps: totalSteps,
      stepName: newStepName
    }));
  }, [currentStep, totalSteps]);

  // Subscribe to project updates
  useEffect(() => {
    console.log('InlineProgressBar WebSocket status:', { isConnected, projectId });
    if (isConnected && projectId) {
      console.log('Subscribing to project:', projectId);
      syncSubscriptions([projectId]);
    }
  }, [isConnected, projectId, syncSubscriptions]);

  // Progress width percent
  const progressPercentage = Math.min(Math.max(progressData.progress, 0), 100);
  

  // Progress background gradient
  const getProgressGradient = () => {
    const baseColor = '#1890ff';
    const lightColor = '#40a9ff';
    
    return `linear-gradient(90deg, 
      ${baseColor} 0%, 
      ${lightColor} ${progressPercentage}%, 
      rgba(24, 144, 255, 0.1) ${progressPercentage}%, 
      rgba(24, 144, 255, 0.1) 100%)`;
  };

  // Animation style
  const getAnimationStyle = () => {
    return {
      background: getProgressGradient()
    };
  };

  return (
    <div style={{
      background: 'rgba(24, 144, 255, 0.15)',
      border: '1px solid rgba(24, 144, 255, 0.3)',
      borderRadius: '4px',
      padding: '6px 12px',
      position: 'relative',
      overflow: 'hidden',
      height: '32px', // Fixed height
      display: 'flex',
      alignItems: 'center'
    }}>
      {/* Progress background */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        ...getAnimationStyle()
      }} />
      
      {/* Content - single row layout */}
      <div style={{ 
        position: 'relative', 
        zIndex: 1,
        width: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: '8px'
      }}>
        {/* Left: step name */}
        <div style={{ 
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          minWidth: '0',
          flex: '1'
        }}>
          <span style={{ 
            color: '#1890ff',
            fontSize: '12px', 
            fontWeight: 600,
            whiteSpace: 'nowrap',
            overflow: 'hidden',
            textOverflow: 'ellipsis'
          }}>
            {progressData.stepName}
          </span>
        </div>
        
        {/* Middle: bar */}
        <div style={{
          width: '80px',
          height: '4px',
          background: 'rgba(24, 144, 255, 0.2)',
          borderRadius: '2px',
          overflow: 'hidden',
          flexShrink: 0
        }}>
          <div style={{
            width: `${progressPercentage}%`,
            height: '100%',
            background: status === 'processing' && progressData.progress < 100 ? 
              'linear-gradient(90deg, #1890ff, #40a9ff, #1890ff)' :
              'linear-gradient(90deg, #1890ff, #40a9ff)',
            borderRadius: '2px',
            transition: 'width 0.3s ease-in-out',
            animation: status === 'processing' && progressData.progress < 100 ? 
              'progressBarPulse 2s infinite ease-in-out' : 'none'
          }} />
        </div>
        
        {/* Right: progress info */}
        <div style={{ 
          display: 'flex',
          alignItems: 'center',
          gap: '4px',
          flexShrink: 0
        }}>
          <span style={{ 
            color: '#1890ff',
            fontSize: '10px',
            opacity: 0.8
          }}>
            {progressData.currentStep}/{progressData.totalSteps}
          </span>
          <span style={{ 
            color: '#1890ff',
            fontSize: '10px',
            fontWeight: 600,
            minWidth: '28px'
          }}>
            {Math.round(progressPercentage)}%
          </span>
        </div>
      </div>
      
      {/* CSS animation */}
      <style>{`
        @keyframes progressBarPulse {
          0%, 100% {
            opacity: 1;
            transform: scaleY(1);
          }
          50% {
            opacity: 0.8;
            transform: scaleY(1.1);
          }
        }
      `}</style>
    </div>
  );
};

export default InlineProgressBar;
