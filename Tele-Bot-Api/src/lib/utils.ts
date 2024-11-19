export function extractHashFromLink(link: string): string {
  const splitLink = link.split('/');
  return splitLink[splitLink.length - 1].replace('+', '');
}

export const delay = (s: number) =>
  new Promise(resolve => setTimeout(resolve, s * 1000));
