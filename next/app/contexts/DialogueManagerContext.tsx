// /contexts/DialogueManagerContext.tsx

import React, { createContext, useContext, useState, ReactNode } from 'react';

// Define the shape of the context
interface DialogueManagerContextType {
  state: string;
  setState: (state: string) => void;
}

// Create the context with a default value (you can set an initial state here)
const DialogueManagerContext = createContext<DialogueManagerContextType | undefined>(undefined);

// Create a provider component
export const DialogueManagerProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, setState] = useState<string>('');

  return (
    <DialogueManagerContext.Provider value={{ state, setState }}>
      {children}
    </DialogueManagerContext.Provider>
  );
};

// Create a custom hook for easier context consumption
export const useDialogueManager = () => {
  const context = useContext(DialogueManagerContext);
  if (context === undefined) {
    throw new Error('useDialogueManager must be used within a DialogueManagerProvider');
  }
  return context;
};