local Processor = {
  model: 'default',
  num_of_core: 4,
};

local Computer = {
  Processor: Processor,
  num_of_ram_slot: 1,
};

{
  Processor: Processor + {
    model: 'intel i7 9700k',
    old_model: super.model,
    old_num_of_core: super.num_of_core,
  },
  Computer: Computer + {
    Processor+: { model: 'intel i5 8400' },
    num_of_ram_slot: 2,
  },
}
