"use client";

/**
 * next/link with prefetching OFF unless a caller asks for it.
 *
 * Why: every link in the viewport made the App Router fetch and parse an RSC
 * payload (24 requests on the DNS page). On a phone that parsing was most of
 * the Total Blocking Time left after the search fix
 * (specs/03-site-ui/lighthouse.txt). A static handbook page is small, so a
 * click without prefetch still opens quickly. Used for the shell (via
 * RootProvider components.Link) and every direct link in our components.
 */

import NextLink from "next/link";
import type { ComponentProps, ReactElement } from "react";

export default function Link({ prefetch, ...props }: ComponentProps<typeof NextLink>): ReactElement {
  return <NextLink prefetch={prefetch ?? false} {...props} />;
}

/** The same, in the anchor-shaped props the fumadocs shell passes (RootProvider components.Link). */
export function ShellLink({
  href,
  prefetch,
  ...props
}: ComponentProps<"a"> & { prefetch?: boolean }): ReactElement {
  return <NextLink href={href ?? "#"} prefetch={prefetch ?? false} {...props} />;
}
