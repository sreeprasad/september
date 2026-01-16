"use client";

import { motion } from "framer-motion";
import { Search, BrainCircuit, MessageSquare, CheckCircle2, Circle } from "lucide-react";
import { useEffect, useState } from "react";

const steps = [
  { id: 1, label: "Browsing Profile & Context", icon: Search },
  { id: 2, label: "Extracting Themes & Sentiment", icon: BrainCircuit },
  { id: 3, label: "Generating Strategy & Scenarios", icon: MessageSquare },
];

export default function AgentProgress() {
  const [currentStep, setCurrentStep] = useState(1);

  useEffect(() => {
    const timer1 = setTimeout(() => setCurrentStep(2), 2500); // Simulate progress
    const timer2 = setTimeout(() => setCurrentStep(3), 6000); // Simulate progress

    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
    };
  }, []);

  return (
    <div className="w-full max-w-md mx-auto space-y-6">
      <div className="space-y-4">
        {steps.map((step) => {
          const isCompleted = currentStep > step.id;
          const isCurrent = currentStep === step.id;
          const Icon = step.icon;

          return (
            <motion.div
              key={step.id}
              initial={{ opacity: 0.5, x: -10 }}
              animate={{ 
                opacity: isCurrent || isCompleted ? 1 : 0.4,
                x: 0,
                scale: isCurrent ? 1.02 : 1
              }}
              className={`flex items-center gap-4 p-3 rounded-xl border transition-all ${
                isCurrent 
                  ? "bg-indigo-50/50 border-indigo-200 shadow-sm" 
                  : "border-transparent"
              }`}
            >
              <div className={`
                w-10 h-10 rounded-full flex items-center justify-center transition-colors
                ${isCompleted ? "bg-green-100 text-green-600" : 
                  isCurrent ? "bg-indigo-100 text-indigo-600 animate-pulse" : 
                  "bg-slate-100 text-slate-400"}
              `}>
                {isCompleted ? (
                  <CheckCircle2 className="w-5 h-5" />
                ) : (
                  <Icon className="w-5 h-5" />
                )}
              </div>
              
              <div className="flex-1">
                <p className={`font-medium text-sm ${
                  isCurrent ? "text-slate-900" : "text-slate-500"
                }`}>
                  {step.label}
                </p>
                {isCurrent && (
                  <motion.div 
                    initial={{ width: 0 }}
                    animate={{ width: "100%" }}
                    transition={{ duration: 3, ease: "linear" }}
                    className="h-1 bg-indigo-200 rounded-full mt-2 overflow-hidden"
                  >
                    <div className="h-full bg-indigo-600 rounded-full w-full origin-left" />
                  </motion.div>
                )}
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
