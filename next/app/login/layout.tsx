import { ReactNode } from "react";

export default function RootLayout(props: { children: ReactNode }) {
  return <>
      <section>{props.children}</section></>;
}