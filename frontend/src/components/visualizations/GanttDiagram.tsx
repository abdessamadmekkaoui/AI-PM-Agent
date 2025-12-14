'use client'

import { useEffect, useRef } from 'react'
import mermaid from 'mermaid'

interface GanttDiagramProps {
    ganttCode: string
    projectName: string
}

export default function GanttDiagram({ ganttCode, projectName }: GanttDiagramProps) {
    const containerRef = useRef<HTMLDivElement>(null)

    useEffect(() => {
        if (!ganttCode || !containerRef.current) return

        // Initialize Mermaid
        mermaid.initialize({
            startOnLoad: false,
            theme: 'default',
            gantt: {
                numberSectionStyles: 4,
                axisFormat: '%Y-%m-%d',
                titleTopMargin: 25,
                barHeight: 30,
                barGap: 8,
                topPadding: 75,
                leftPadding: 75,
                gridLineStartPadding: 10,
                fontSize: 11,
                sectionFontSize: 11,
            }
        })

        // Render the diagram
        const renderDiagram = async () => {
            try {
                const { svg } = await mermaid.render('gantt-diagram', ganttCode)
                if (containerRef.current) {
                    containerRef.current.innerHTML = svg
                }
            } catch (error) {
                console.error('Mermaid rendering error:', error)
                // Fallback to showing code
                if (containerRef.current) {
                    containerRef.current.innerHTML = `
            <div class="text-red-600 dark:text-red-400 p-4 bg-red-50 dark:bg-red-900/20 rounded">
              <p class="font-semibold mb-2">Erreur de rendu du diagramme</p>
              <pre class="text-xs overflow-auto">${ganttCode}</pre>
            </div>
          `
                }
            }
        }

        renderDiagram()
    }, [ganttCode])

    return (
        <div className="w-full">
            <div
                ref={containerRef}
                className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700 overflow-x-auto"
            />
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-4 text-center">
                💡 Diagramme de Gantt généré automatiquement par les agents IA
            </p>
        </div>
    )
}
