import { useState, useCallback, useRef, useEffect } from 'react';
import { useWebSocket, TaskProgressUpdateMessage } from './useWebSocket';

export interface TaskProgressState {
  task_id: string;
  progress: number;
  step: number;
  total: number;
  phase: string;
  message: string;
  status: string;
  seq: number;
  ts: number;
  meta?: any;
  last_updated: number;
}

export interface UseTaskProgressOptions {
  userId: string;
  taskId: string;
  onProgressUpdate?: (state: TaskProgressState) => void;
  onTaskComplete?: (state: TaskProgressState) => void;
  onTaskFailed?: (state: TaskProgressState) => void;
}

export const useTaskProgress = (options: UseTaskProgressOptions) => {
  const { userId, taskId, onProgressUpdate, onTaskComplete, onTaskFailed } = options;
  
  const [taskState, setTaskState] = useState<TaskProgressState | null>(null);
  const [isSubscribed, setIsSubscribed] = useState(false);
  const [lastSeq, setLastSeq] = useState(0);
  const [lastTs, setLastTs] = useState(0);
  const finalStateChecked = useRef(false);

  // processWebSockettranslated
  const handleWebSocketMessage = useCallback((message: any) => {
    if (message.type === 'task_progress_update' && message.task_id === taskId) {
      const progressMessage = message as TaskProgressUpdateMessage;
      
      // translatedAndtranslatedcheck
      if (progressMessage.seq <= lastSeq && progressMessage.ts <= lastTs) {
        console.log(`translated: seq=${progressMessage.seq}, ts=${progressMessage.ts}`);
        return;
      }
      
      // updatestatus
      const newState: TaskProgressState = {
        task_id: progressMessage.task_id || taskId,
        progress: progressMessage.progress,
        step: 0,
        total: 0,
        phase: progressMessage.step_name || 'processing',
        message: progressMessage.message || '',
        status: progressMessage.status,
        seq: lastSeq + 1,
        ts: Math.floor(Date.now() / 1000),
        last_updated: Date.now()
      };
      
      setTaskState(newState);
      setLastSeq((prev) => prev + 1);
      setLastTs(Math.floor(Date.now() / 1000));
      
      // translated
      onProgressUpdate?.(newState);
      
      // checktranslated
      if (progressMessage.status === 'completed') {
        onTaskComplete?.(newState);
        // translated
        setTimeout(() => performFinalStateCheck(), 1000);
      } else if (progressMessage.status === 'failed') {
        onTaskFailed?.(newState);
        // translated
        setTimeout(() => performFinalStateCheck(), 1000);
      }
    }
  }, [taskId, lastSeq, lastTs, onProgressUpdate, onTaskComplete, onTaskFailed]);

  // WebSocketconnect
  const { 
    isConnected, 
    subscribeToTask, 
    unsubscribeFromTask
  } = useWebSocket({
    userId,
    onMessage: handleWebSocketMessage
  });

  // translated：fromHTTP APIfetchtranslatedstatus
  const performFinalStateCheck = useCallback(async () => {
    if (finalStateChecked.current) return;
    finalStateChecked.current = true;
    
    try {
      console.log(`translated: ${taskId}`);
      // translatedAPIcall，translatedgetTaskProgresstranslatednot found
      // const response = await projectApi.getTaskProgress(taskId);
      
      // if (response.data) {
      //   const apiState: TaskProgressState = {
      //     task_id: taskId,
      //     progress: response.data.progress || 0,
      //     step: response.data.current_step || 0,
      //     total: 6,
      //     phase: 'unknown',
      //     message: response.data.current_step || 'translatedstatus',
      //     status: response.data.status || 'unknown',
      //     seq: lastSeq + 1,
      //     ts: Date.now() / 1000,
      //     last_updated: Date.now()
      //   };
      //   
      //   setTaskState(apiState);
      //   console.log('translated:', apiState);
      // }
    } catch (error) {
      console.error('translatedfailed:', error);
    }
  }, [taskId, lastSeq]);

  // translatedtaskprogress
  const subscribe = useCallback(() => {
    if (isConnected && !isSubscribed) {
      const success = subscribeToTask(taskId);
      if (success) {
        setIsSubscribed(true);
        console.log(`translatedtaskprogress: ${taskId}`);
      }
    }
  }, [isConnected, isSubscribed, subscribeToTask, taskId]);

  // canceltranslatedtaskprogress
  const unsubscribe = useCallback(() => {
    if (isConnected && isSubscribed) {
      const success = unsubscribeFromTask(taskId);
      if (success) {
        setIsSubscribed(false);
        console.log(`translatedcanceltranslatedtaskprogress: ${taskId}`);
      }
    }
  }, [isConnected, isSubscribed, unsubscribeFromTask, taskId]);

  // translated/canceltranslated
  useEffect(() => {
    if (isConnected) {
      subscribe();
    } else {
      setIsSubscribed(false);
    }
    
    return () => {
      if (isSubscribed) {
        unsubscribe();
      }
    };
  }, [isConnected, subscribe, unsubscribe, isSubscribed]);

  // translatedclean
  useEffect(() => {
    return () => {
      if (isSubscribed) {
        unsubscribe();
      }
    };
  }, [isSubscribed, unsubscribe]);

  return {
    taskState,
    isConnected,
    isSubscribed,
    subscribe,
    unsubscribe,
    performFinalStateCheck
  };
};

