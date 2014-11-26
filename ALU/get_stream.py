def get_streams(name):
 Stream_dict={'upmu/grizzly_new/C1ANG':"4b7fec6d-270e-4bd6-b301-0eac6df17ca2",'upmu/grizzly_new/C1MAG':"425b9c51-9aba-4d1a-a677-85cd7afd6269",\
              'upmu/grizzly_new/C2ANG':"9ffeaf2a-46a9-465f-985d-96f84df66283",'upmu/grizzly_new/C2MAG':"ca613e9a-1211-4c52-a98f-b8f9f1ce0672",\
              'upmu/grizzly_new/C3ANG':"8b40fe4c-36ee-4b10-8aef-1eef8c471e1d",'upmu/grizzly_new/C3MAG':"b1025f33-97fd-45d6-bc0f-80132e1dc756",\
              'upmu/grizzly_new/L1ANG':"b4776088-2f85-4c75-90cd-7472a949a8fa",'upmu/grizzly_new/L1MAG':"a64c386e-2dd4-4f17-96cb-1655358cb12c",\
              'upmu/grizzly_new/L2ANG':"8b80c070-7bb1-44d3-b3a8-301558d573ea",'upmu/grizzly_new/L2MAG':"a002295a-32ee-41a1-8ec4-8657d0d1f943",\
              'upmu/grizzly_new/L3ANG':"b653c63b-4acc-45ee-ae3d-1602e6116bc1",'upmu/grizzly_new/L3MAG':"db3ea4f7-a337-4874-baeb-17fc2c0cf18b",\
              'upmu/grizzly_new/LSTATE':"89d1c0a1-aa97-4f5b-bdfb-0d04b1dc94f8",\
              'upmu/switch_a6/C1ANG':"4072af6f-938e-450c-9927-37dee6968446",'upmu/switch_a6/C1MAG':"bf8ea2c0-6d04-4cdd-ba4b-0421eac0cabd",\
              'upmu/switch_a6/C2ANG':"bf045a36-34df-4bee-a747-b20c3164723a",'upmu/switch_a6/C2MAG':"51d4801e-0bb6-4040-8e74-e7839be65156",\
              'upmu/switch_a6/C3ANG':"8a5d0010-4665-4b59-ab6f-e7858c12284a",'upmu/switch_a6/C3MAG':"249b364d-b0a1-4b65-8aca-ffd68565c1de",\
              'upmu/switch_a6/L1ANG':"adf13e17-44b7-4ef6-ae3f-fde8a9152ab7",'upmu/switch_a6/L1MAG':"df64af25-a389-4be9-8061-f87c3616f286",\
              'upmu/switch_a6/L2ANG':"4f56a8f1-f3ca-4684-930e-1b4d9955f72c",'upmu/switch_a6/L2MAG':"6e6ad513-ddd2-47fb-98c1-16e6477504fc",\
              'upmu/switch_a6/L3ANG':"2c07ccef-20c5-4971-87cf-2c187ce5f722",'upmu/switch_a6/L3MAG':"bcf38098-0e16-46f2-a9fb-9ce481d7d55b",\
              'upmu/switch_a6/LSTATE':"33eb7c04-6357-4de8-aa44-6f5a6abab7e6"}
 if name=='upmu/grizzly_new/C1ANG':
   return "4b7fec6d-270e-4bd6-b301-0eac6df17ca2"
 elif name=='upmu/grizzly_new/C1MAG':
   return "425b9c51-9aba-4d1a-a677-85cd7afd6269"
 elif name=='upmu/grizzly_new/C2ANG':
   return "9ffeaf2a-46a9-465f-985d-96f84df66283"
 elif name=='upmu/grizzly_new/C2MAG':
   return "ca613e9a-1211-4c52-a98f-b8f9f1ce0672"
 elif name=='upmu/grizzly_new/C3ANG':
   return "8b40fe4c-36ee-4b10-8aef-1eef8c471e1d"
 elif name=='upmu/grizzly_new/C3MAG':
   return "b1025f33-97fd-45d6-bc0f-80132e1dc756"
 elif name=='upmu/grizzly_new/L1ANG':
   return "b4776088-2f85-4c75-90cd-7472a949a8fa"
 elif name=='upmu/grizzly_new/L1MAG':
   return "a64c386e-2dd4-4f17-96cb-1655358cb12c"
 elif name=='upmu/grizzly_new/L2ANG':
   return name=="8b80c070-7bb1-44d3-b3a8-301558d573ea"
 elif name=='upmu/grizzly_new/L2MAG':
   return "a002295a-32ee-41a1-8ec4-8657d0d1f943"
 elif name=='upmu/grizzly_new/L3ANG':
   return "b653c63b-4acc-45ee-ae3d-1602e6116bc1"
 elif name=='upmu/grizzly_new/L3MAG':
   return "db3ea4f7-a337-4874-baeb-17fc2c0cf18b"
 elif name=='upmu/grizzly_new/LSTATE':
   return "89d1c0a1-aa97-4f5b-bdfb-0d04b1dc94f8"
 elif name=='upmu/switch_a6/C1ANG':
   return "4072af6f-938e-450c-9927-37dee6968446"
 elif name=='upmu/switch_a6/C1MAG':
   return "bf8ea2c0-6d04-4cdd-ba4b-0421eac0cabd"
 elif name=='upmu/switch_a6/C2ANG':
   return "bf045a36-34df-4bee-a747-b20c3164723a"
 elif name=='upmu/switch_a6/C2MAG':
   return "51d4801e-0bb6-4040-8e74-e7839be65156"
 elif name=='upmu/switch_a6/C3ANG':
   return "8a5d0010-4665-4b59-ab6f-e7858c12284a"
 elif name=='upmu/switch_a6/C3MAG':
   return "249b364d-b0a1-4b65-8aca-ffd68565c1de"
 elif name=='upmu/switch_a6/L1ANG':
   return "adf13e17-44b7-4ef6-ae3f-fde8a9152ab7"
 elif name=='upmu/switch_a6/L1MAG':
   return "df64af25-a389-4be9-8061-f87c3616f286"
 elif name=='upmu/switch_a6/L2ANG':
   return "4f56a8f1-f3ca-4684-930e-1b4d9955f72c"
 elif name=='upmu/switch_a6/L2MAG':
   return "6e6ad513-ddd2-47fb-98c1-16e6477504fc"
 elif name=='upmu/switch_a6/L3ANG':
   return "2c07ccef-20c5-4971-87cf-2c187ce5f722"
 elif name=='upmu/switch_a6/L3MAG':
   return "bcf38098-0e16-46f2-a9fb-9ce481d7d55b"
 elif name=='upmu/switch_a6/LSTATE':
   return "33eb7c04-6357-4de8-aa44-6f5a6abab7e6"
 else:
   return None
