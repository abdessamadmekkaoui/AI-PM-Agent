// src/components/agents/AgentStatus.tsx
'use client'

import { Bot, CheckCircle2, Loader2 } from 'lucide-react'


interface AgentStatusProps {
  status: {
    planner: 'idle' | 'working' | 'completed'
    scheduler: 'idle' | 'working' | 'completed'
    backlog: 'idle' | 'working' | 'completed'
  }
}

export default function AgentStatus({ status }: AgentStatusProps) {
  const agents = [
    {
      id: 'planner',
      name: 'Agent Planner',
      description: 'Génération des tâches',
      icon: '🤖',
      status: status.planner
    },
    {
      id: 'scheduler',
      name: 'Agent Scheduler',
      description: 'Création du Gantt',
      icon: '📅',
      status: status.scheduler
    },
    {
      id: 'backlog',
      name: 'Agent Backlog',
      description: 'Génération User Stories',
      icon: '📝',
      status: status.backlog
    }
  ]

  return (
    <div className="bg-blue-50 dark:bg-blue-900/20 border-b border-blue-200 dark:border-blue-800 px-6 py-4">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center gap-2 mb-3">
          <Bot className="w-5 h-5 text-blue-600 dark:text-blue-400" />
          <h3 className="text-sm font-semibold text-blue-900 dark:text-blue-100">
            Agents en Action
          </h3>
        </div>
        
        <div className="grid grid-cols-3 gap-4">
          {agents.map((agent) => (
            <div
              key={agent.id}
              className={`bg-white dark:bg-gray-800 p-4 rounded-lg border transition-all ${
                agent.status === 'working'
                  ? 'border-blue-400 dark:border-blue-600 shadow-md'
                  : agent.status === 'completed'
                  ? 'border-green-400 dark:border-green-600'
                  : 'border-gray-200 dark:border-gray-700'
              }`}
            >
              <div className="flex items-start justify-between mb-2">
                <span className="text-2xl">{agent.icon}</span>
                {agent.status === 'working' && (
                  <Loader2 className="w-5 h-5 text-blue-600 animate-spin" />
                )}
                {agent.status === 'completed' && (
                  <CheckCircle2 className="w-5 h-5 text-green-600" />
                )}
              </div>
              
              <h4 className="font-medium text-gray-900 dark:text-white text-sm mb-1">
                {agent.name}
              </h4>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                {agent.description}
              </p>
              
              {agent.status === 'working' && (
                <div className="mt-3">
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1.5">
                    <div className="bg-blue-600 h-1.5 rounded-full animate-pulse" style={{ width: '60%' }} />
                  </div>
                </div>
              )}
              
              {agent.status === 'completed' && (
                <div className="mt-2 text-xs text-green-600 dark:text-green-400 font-medium">
                  ✓ Terminé
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}