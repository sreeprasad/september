"use client";

import { motion } from "framer-motion";

export default function AnimatedBackground() {
  return (
    <div className="absolute inset-0 overflow-hidden rounded-3xl pointer-events-none">
      <div className="absolute -inset-[100%] opacity-30">
        <motion.div
          animate={{
            transform: [
              "translate(0%, 0%) rotate(0deg)",
              "translate(10%, 10%) rotate(10deg)",
              "translate(-5%, 5%) rotate(-5deg)",
              "translate(0%, 0%) rotate(0deg)",
            ],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            repeatType: "mirror",
            ease: "easeInOut",
          }}
          className="w-full h-full bg-[radial-gradient(circle_at_50%_50%,rgba(99,102,241,0.4),transparent_50%)] blur-3xl scale-150"
        />
        <motion.div
          animate={{
            transform: [
              "translate(0%, 0%) scale(1)",
              "translate(-10%, -10%) scale(1.1)",
              "translate(5%, -5%) scale(0.9)",
              "translate(0%, 0%) scale(1)",
            ],
          }}
          transition={{
            duration: 25,
            repeat: Infinity,
            repeatType: "mirror",
            ease: "easeInOut",
            delay: 2,
          }}
          className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(circle_at_20%_20%,rgba(139,92,246,0.4),transparent_40%)] blur-3xl scale-150"
        />
        <motion.div
          animate={{
            transform: [
              "translate(0%, 0%)",
              "translate(15%, -15%)",
              "translate(-10%, 10%)",
              "translate(0%, 0%)",
            ],
          }}
          transition={{
            duration: 22,
            repeat: Infinity,
            repeatType: "mirror",
            ease: "easeInOut",
            delay: 1,
          }}
          className="absolute bottom-0 right-0 w-full h-full bg-[radial-gradient(circle_at_80%_80%,rgba(167,139,250,0.3),transparent_40%)] blur-3xl scale-150"
        />
      </div>
    </div>
  );
}
