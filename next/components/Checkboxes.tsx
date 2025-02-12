import { MUTED_TEAL, NODE_COLORS_CYAN, SOFT_BLUE } from '@/app/utils/constants';
import React, { useState } from 'react';

type CheckboxProps = {
    items: any;
    handleCheckboxChange: (item: any) => void;
}

function CheckboxList(props:CheckboxProps) {
  const { items, handleCheckboxChange } = props;
  const [selectedItems, setSelectedItems] = useState<any>([]);

  return (
    <div className={`top-0 right max-w-md mx-auto p-4 rounded-lg shadow-md`}>
      {/* <h2 className="text-xl font-semibold mb-4">Select Items</h2> */}
      <ul className="space-y-1">
        {["Persons", "Works", "Sections", "Lines"].map((item: any, index: number) => (
          <li 
            key={index} 
            className="flex items-left"
            style={{
                color: MUTED_TEAL
              }}
        >
            <input
              type="checkbox"
              id={`checkbox-${index}`}
              className="`mt-4 top-0 z-200 w-200px hover:bg-mutedTeal font-bold py-2 px-4 rounded` focus:ring-blue-500"
              checked={items.includes(item)}
              onChange={() => handleCheckboxChange(item)}
            />
            <label
              style={{
                color: SOFT_BLUE,
                textAlign: 'left'
              }}
              htmlFor={`checkbox-${index}`}
              className="ml-2 text-gray-700 select-none"
            >
              {item}
            </label>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default CheckboxList;